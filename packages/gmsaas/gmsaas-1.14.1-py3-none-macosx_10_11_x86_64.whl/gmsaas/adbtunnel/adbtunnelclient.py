# Copyright 2019 Genymobile
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
gmadbtunneld binary wrapper
"""

import os
import json
import subprocess
import platform
import re

import gmsaas
from gmsaas.gmsaas.proxy import get_proxy_info
from gmsaas.gmsaas.timeout import (
    get_adbconnect_timeout,
    get_adbdisconnect_timeout,
    get_adbtunnel_start_timeout,
    wait_until,
)
from gmsaas.model.instanceinfo import Instance, Instances, TunnelState, is_adbtunnel_connecting
from gmsaas.model.daemoninfo import AdbTunnelDaemonInfo
from gmsaas.gmsaas.errors import PackageError, AppleSiliconChipError
from gmsaas.saas.api import CLOUD_BASE_URL
from gmsaas.gmsaas.triggererrors import get_fake_adbtunnel_state

from gmsaas.gmsaas.logger import LOGGER, log_elapsed_time


TunnelExitCode = type("TunnelExitCode", (), {"EXIT_OK": 0, "EXIT_BAD_ARGUMENTS": 1, "EXIT_KO": 2})

ADBTUNNEL_FAKE_INSTANCE_STATE = get_fake_adbtunnel_state()


def remove_whitespaces(text):
    """Remove any whitespace chars of a string"""
    return re.sub(r"\s+", "", text)


class AdbTunnelClientResultKeeper:
    """Lightweight class that fetches and stores last Instances result of AdbTunnelClient"""

    def __init__(self, client):
        self.client = client
        self.instance = Instance()

    def get(self, instance_uuid):
        """Get Instance for `instance_uuid` and store it"""
        self.instance = self.client.get_instance(instance_uuid)

        if ADBTUNNEL_FAKE_INSTANCE_STATE:
            LOGGER.info("Using fake adbtunnel state %s", ADBTUNNEL_FAKE_INSTANCE_STATE)
            self.instance.tunnel_state = ADBTUNNEL_FAKE_INSTANCE_STATE

        return self.instance


class AdbTunnelClient:
    """
    Class able to interact with gmadbtunneld
    """

    def __init__(self, exec_bin):
        self.exec_bin = exec_bin
        if "GMADBTUNNELD_PATH" in os.environ:
            self.exec_bin = os.environ["GMADBTUNNELD_PATH"]

    def is_ready(self):
        """
        Return True if adbtunnel daemon is found and executable, False otherwise
        """
        return os.path.exists(self.exec_bin) and os.path.isfile(self.exec_bin) and os.access(self.exec_bin, os.X_OK)

    def _detached_exec(self, args):
        cmd = [self.exec_bin]
        cmd.extend(args)
        try:
            with subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL):
                pass
        except FileNotFoundError as error:
            raise PackageError(self.exec_bin) from error

    @log_elapsed_time
    def _rpc_call(self, args):
        """
        Sends an RPC call to gmadbtunneld, returns a dict containing the answer.
        If gmadbtunneld is not running, exit code is still 0 but the output is empty,
        returns an empty dict in that case
        """
        cmd = [self.exec_bin]
        cmd.extend(args)
        try:
            proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
            if os.environ.get("GMSAAS_BAD_CPU_TYPE"):
                raise AppleSiliconChipError()
        except FileNotFoundError as error:
            raise PackageError(self.exec_bin) from error
        except OSError as error:
            if platform.system() == "Darwin" and "Bad CPU" in str(error):
                raise AppleSiliconChipError() from error
            raise PackageError(self.exec_bin) from error
        if proc.returncode != TunnelExitCode.EXIT_OK:
            details = f"exit_code: {proc.returncode}, stdout: {remove_whitespaces(proc.stdout.decode('utf-8'))}, stderr: {remove_whitespaces(proc.stderr.decode('utf-8'))}"
            raise PackageError(self.exec_bin, details)
        out = proc.stdout.decode("utf-8")
        return json.loads(out)

    def start(self):
        """
        Start ADB Tunnel Daemon
        """
        LOGGER.info("Start ADB Tunnel daemon")
        args = ["start"]
        self._detached_exec(args)
        return self.wait_for_started()

    def wait_for_started(self):
        """
        Wait for the ADB Tunnel daemon to be started
        """
        LOGGER.debug("Waiting for ADB Tunnel started")
        return wait_until(lambda: self.get_daemon_info().running, get_adbtunnel_start_timeout())

    def connect(self, instance_uuid, adb_serial_port=None):
        """
        Connect an Instance to ADB
        """
        if not self.start():
            LOGGER.error("ADB Tunnel not started in time")
        LOGGER.info("[%s] Connecting instance to ADB tunnel", instance_uuid)
        args = ["connect", str(instance_uuid)]
        if adb_serial_port:
            LOGGER.info("[%s] Using port %d for instance", instance_uuid, adb_serial_port)
            args.extend(["--adb-serial-port", str(adb_serial_port)])
        self._rpc_call(args)

    def disconnect(self, instance_uuid):
        """
        Disconnect an Instance from ADB
        """
        LOGGER.info("[%s] Connecting instance from ADB tunnel", instance_uuid)
        args = ["disconnect", str(instance_uuid)]
        self._rpc_call(args)

    def stop(self):
        """
        Stop the running gmadbtunneld process
        """
        LOGGER.info("Stopping ADB tunnel...")
        args = ["stop"]
        self._rpc_call(args)

        LOGGER.debug("Waiting for ADB Tunnel stopped")
        if not wait_until(lambda: not self.get_daemon_info().running, get_adbtunnel_start_timeout()):
            LOGGER.error("ADB tunnel did not stopped in time")
        else:
            LOGGER.debug("ADB tunnel stopped")

    def get_daemon_info(self):
        """
        Get information about gmadbtunneld
        """
        data = self._rpc_call(["getdaemoninfo"])
        if not data["running"]:
            # gmadbtunneld is not running, so compatible for sure.
            return AdbTunnelDaemonInfo(gmsaas.__version__, CLOUD_BASE_URL, get_proxy_info(), False)

        # Setting up missing default values
        if "proxy" not in data:
            # It means `gmadbtunneld` <= 1.2.0
            # There was no proxy support so using a default value.
            data.update({"proxy": ""})

        assert "platform_url" in data
        assert "version" in data
        assert "proxy" in data
        return AdbTunnelDaemonInfo(data["version"], data["platform_url"], data["proxy"], True)

    def get_instances(self):
        """
        Return Instances from gmadbtunneld
        """
        data = self._rpc_call(["getinstances"])
        if not data["running"]:
            return Instances()
        assert "instances" in data
        return Instances.create_from_adbtunnel(data["instances"])

    def get_instance(self, instance_uuid):
        """
        Return Instance for instance_uuid from gmadbtunneld
        """
        instances = self.get_instances()
        return instances.get(instance_uuid, Instance(instance_uuid))

    def wait_for_adb_connected(self, instance_uuid):
        """
        Return the actual Instance whether it succeeds or not, the caller needs to check it.
        """
        LOGGER.debug("[%s] Waiting for ADB connected", instance_uuid)
        keeper = AdbTunnelClientResultKeeper(self)
        wait_until(
            lambda: not is_adbtunnel_connecting(keeper.get(instance_uuid).tunnel_state), get_adbconnect_timeout()
        )
        return keeper.instance

    def wait_for_adb_disconnected(self, instance_uuid):
        """
        Return the actual Instance whether it succeeds or not, the caller needs to check it.
        """
        LOGGER.debug("Waiting for %s disconnected from ADB", instance_uuid)
        keeper = AdbTunnelClientResultKeeper(self)
        wait_until(
            lambda: keeper.get(instance_uuid).tunnel_state == TunnelState.DISCONNECTED, get_adbdisconnect_timeout()
        )
        return keeper.instance
