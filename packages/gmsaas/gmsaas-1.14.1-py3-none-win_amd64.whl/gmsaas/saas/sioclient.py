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
Genymotion Cloud SaaS SocketIO client
"""

import os
import json
from collections import namedtuple
import socketio
import engineio

from gmsaas.gmsaas.timeout import get_start_timeout, get_stop_timeout, get_save_timeout, wait_until
from gmsaas.gmsaas.triggererrors import trigger_sio_unreachable, get_fake_sio_instance_state, trigger_unrecognized_state
from gmsaas.gmsaas.logger import LOGGER, get_logger
from gmsaas.model.instanceinfo import (
    Instance,
    InstanceState,
    is_instance_starting,
    is_instance_stopping,
    is_instance_saving,
)

SIO_FAKE_INSTANCE_STATE = get_fake_sio_instance_state()
SIO_UNRECOGNIZED_INSTANCE_STATE = trigger_unrecognized_state()
SIO_LOGGER = get_logger(logger_name="sio", version=None)
EIO_LOGGER = get_logger(logger_name="eio", version=None)

SocketIOUrl = namedtuple("SocketIOUrl", ["base", "path"])


class SIOClient:
    """
    Genymotion Cloud SaaS SocketIO client

    Use socket.io python implementation: https://python-socketio.readthedocs.io
    This class is designed to get push notifications about instances state.

    Architecture:
        - Connection:
            Raises SIOConnectionError exception when failed.
        - Subscription:
            Once connected, subscription to `instances` tag is done
        - Events:
            Once subscribed, all events are received and treated.
            All instances state are stored in a dict.
        - Wait conditions:
            Convenient functions are available to wait for a instance to be in particular state

    Usage:
        SIOClient is a context manager, so connection and disconnection is implicit.

        with SIOClient(connection_url=connection_url) as sio:
            # Don't forget to check exception that can occur during connection
            if sio.exception:
                # Handle connection error
            if not sio.wait_for_...():
                # Handle wait condition error
    """

    def __enter__(self):
        try:
            self._connect()
        except Exception as error:
            self.exception = error
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        try:
            self._disconnect()
        except Exception as error:
            # Don't raise the error, disconnection step is not critical
            LOGGER.exception(error)

    def __init__(self, connection_url: SocketIOUrl):
        self.exception = None
        self.connection_url: SocketIOUrl = connection_url
        # By default, we don't log SocketIO / EngineIO traces because
        # they might contain sensitive data (API Token)
        sio_logger = SIO_LOGGER if LOGGER.verbosity > 0 else False
        eio_logger = EIO_LOGGER if LOGGER.verbosity > 0 else False
        self.client = socketio.Client(logger=sio_logger, engineio_logger=eio_logger, reconnection=False)
        self.instances = {}
        self.client.on("connect", self._on_connected)
        self.client.on("disconnect", self._on_disconnected)
        self.client.on("instances", self._on_instance_changed)
        self.is_client_connected = False

    def _on_connected(self):
        LOGGER.debug("SIO client connected")
        self.is_client_connected = True
        self.client.emit(event="subscribe", data={"tags": ["instances"]})

    def _on_disconnected(self):
        self.is_client_connected = False
        LOGGER.debug("SIO client disconnected")

    def _on_instance_changed(self, data):
        if LOGGER.verbosity > 1:
            LOGGER.info("Instance changed: %s", json.dumps(data, indent=4))

        try:
            state = data["data"]["state"]
            instance_uuid = data["data"]["uuid"]
        except Exception:
            LOGGER.error("Unreadable instance message: %s", data)
            return

        if SIO_UNRECOGNIZED_INSTANCE_STATE:
            if state in (InstanceState.BOOTING, InstanceState.DELETING):
                state = "UNRECOGNIZED_STATE"

        if state not in InstanceState.__dict__:
            LOGGER.error("Unrecognized instance state %s", state)
            return

        if not self.instances.get(instance_uuid):
            LOGGER.debug("Added instance %s", instance_uuid)
            self.instances[instance_uuid] = Instance(instance_uuid)
        self.instances[instance_uuid].set_state(state)

    def _get_instance_state(self, instance_uuid):
        if SIO_FAKE_INSTANCE_STATE:
            LOGGER.info("Using fake instance state %s", SIO_FAKE_INSTANCE_STATE)
            return SIO_FAKE_INSTANCE_STATE
        return self.instances.get(instance_uuid, Instance(instance_uuid)).state

    def _connect(self):
        """
        Connect SocketIO client
        """
        LOGGER.info("Starting SIO client")
        if trigger_sio_unreachable():
            raise engineio.exceptions.ConnectionError()

        transports = None  # Default: websocket if possible otherwise polling
        if os.environ.get("GMSAAS_SIO_FORCE_POLLING"):
            LOGGER.info("Forcing SIO transport to polling")
            transports = ["polling"]

        self.client.connect(url=self.connection_url.base, socketio_path=self.connection_url.path, transports=transports)

    def _disconnect(self):
        self.client.disconnect()

    def wait_for_instance_started(self, instance_uuid):
        """
        Return the actual state whether it succeeds or not, the caller needs to check it.
        """
        LOGGER.debug("Waiting for %s started", instance_uuid)
        wait_until(
            lambda: (not is_instance_starting(self._get_instance_state(instance_uuid))) or not self.is_client_connected,
            get_start_timeout(),
        )
        return self._get_instance_state(instance_uuid)

    def wait_for_instance_stopped(self, instance_uuid):
        """
        Return the actual state whether it succeeds or not, the caller needs to check it.
        """
        LOGGER.debug("Waiting for %s stopped", instance_uuid)
        wait_until(
            lambda: (not is_instance_stopping(self._get_instance_state(instance_uuid))) or not self.is_client_connected,
            get_stop_timeout(),
        )
        return self._get_instance_state(instance_uuid)

    def wait_for_instance_saved(self, instance_uuid):
        """
        Return the actual state whether it succeeds or not, the caller needs to check it.
        """
        LOGGER.debug("Waiting for %s saved", instance_uuid)
        wait_until(
            lambda: (not is_instance_saving(self._get_instance_state(instance_uuid))) or not self.is_client_connected,
            get_save_timeout(),
        )
        return self._get_instance_state(instance_uuid)
