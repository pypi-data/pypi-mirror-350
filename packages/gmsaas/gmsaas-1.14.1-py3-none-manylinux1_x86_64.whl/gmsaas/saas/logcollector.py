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
Log collector
"""
import pathlib
import os
import platform
import datetime
import shlex

from zipfile import ZipFile
from tabulate import tabulate
import psutil

from gmsaas.gmsaas.logger import LOGGER
from gmsaas.storage.settings import get_gmsaas_log_path, get_gmadbtunneld_log_path
from gmsaas.adbtunnel import get_adbtunnel, get_adbclient
from gmsaas.model.instanceinfo import TunnelState


def get_adb_log_path():
    """
    Get ADB log path, for more details see:
    https://android.googlesource.com/platform/system/core/+/refs/heads/sdk-release/adb/adb_utils.cpp#322
    """
    if platform.system() == "Windows":
        # https://docs.microsoft.com/en-us/windows/desktop/api/fileapi/nf-fileapi-gettemppatha#remarks
        for dirname in "$TMP", "$TEMP", "$USERPROFILE", r"C:\Windows":
            location = os.path.expandvars(dirname)
            if os.path.exists(location):
                break
        return os.path.join(location, "adb.log")

    location = os.environ.get("TMPDIR", "/tmp")
    return os.path.join(location, "adb.{}.log".format(os.getuid()))  # pylint: disable=E1101(no-member)


def _get_log_files():
    # Keep gmsaas.log last in order to archive latest log traces
    return [get_gmadbtunneld_log_path(), get_adb_log_path(), get_gmsaas_log_path()]


def _get_log_archive_dir():
    return os.environ.get("GMSAAS_LOGS_ARCHIVE_DIR", os.getcwd())


def _get_log_archive_name():
    return os.environ.get("GMSAAS_LOGS_ARCHIVE_NAME", datetime.datetime.now().strftime("gmsaas-logs-%Y%m%d-%H%M%S.zip"))


def _get_ps_content():
    # Available attribute list: https://psutil.readthedocs.io/en/latest/#psutil.Process.as_dict
    attrs = ["username", "pid", "cpu_percent", "memory_percent", "status", "create_time", "cmdline"]
    data = []
    create_time_idx = 5  # Replace timestamp by iso format
    cmdline_idx = 6  # Join cmd line
    for process in psutil.process_iter(attrs=attrs):
        process_data = [process.info[x] for x in attrs]
        process_data[create_time_idx] = (
            datetime.datetime.fromtimestamp(process_data[create_time_idx]).replace(microsecond=0).isoformat()
        )
        if process_data[cmdline_idx] is not None:
            process_data[cmdline_idx] = " ".join([shlex.quote(x) for x in process_data[cmdline_idx]])
        data.append(process_data)
    tabulate_content = tabulate(data, headers=attrs).splitlines()
    tabulate_content[1] = tabulate_content[1][:119]  #  Truncate header dashes to 120 chars
    return "\n".join(tabulate_content)


class LogCollector:
    """
    Log collector
    """

    def __init__(self):
        self.log_files = _get_log_files()

    def add_ps_log(self, archive):
        """
        Get process info using psutil and add it to the archive
        """
        try:
            archive.writestr("ps.log", _get_ps_content())
            LOGGER.info("Added `ps.log` to logs archive")
        except Exception as ps_exception:
            LOGGER.info("`ps.log` not added to logs archive: error occured: %s", str(ps_exception))

    def add_logcat_logs(self, archive):
        """
        Get logcat of instances connected to ADB and add it to the archive
        """
        adbtunnel = get_adbtunnel()
        if not adbtunnel.is_ready():
            LOGGER.warning("Logcat logs skipped: adbtunnel not ready")
            return

        adb_client = get_adbclient()
        if not adb_client.is_ready():
            LOGGER.warning("Logcat logs skipped: ADB not ready")
            return

        instances = [i for i in adbtunnel.get_instances() if i.tunnel_state == TunnelState.CONNECTED]
        if not instances:
            LOGGER.info("Logcat logs skipped: no instances connected to ADB")
            return

        for instance in instances:
            output = adb_client.logcat(instance.adb_serial)
            if output is None:
                LOGGER.warning("Logcat failed for instance `%s`", instance.uuid)
                continue
            filename = "logcat-{}.log".format(instance.uuid)
            archive.writestr(filename, output)
            LOGGER.info("Added `%s` to logs archive", filename)

    def add_static_log_files(self, archive):
        """
        Add static log files to the archive
        """
        for log_file in self.log_files:
            if os.path.exists(log_file):
                LOGGER.info("Added `%s` to logs archive", log_file)
                archive.write(log_file, os.path.basename(log_file))
            else:
                LOGGER.info("`%s` not added to logs archive: file does not exist", log_file)

    def process(self, archive_path=None):
        """
        Generate logs archive
        """
        if not archive_path:
            archive_path = os.path.join(_get_log_archive_dir(), _get_log_archive_name())
        elif pathlib.Path(archive_path).is_dir():
            archive_path = os.path.join(archive_path, _get_log_archive_name())
        with ZipFile(archive_path, "w") as archive:
            self.add_ps_log(archive)
            self.add_logcat_logs(archive)
            self.add_static_log_files(archive)
        return archive_path
