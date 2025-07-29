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
SaaS Instance data
"""
from collections import OrderedDict
from datetime import datetime

from tabulate import tabulate

from gmsaas.gmsaas.logger import LOGGER
from gmsaas.model.recipeinfo import Recipe

DEFAULT_ADB_SERIAL = "0.0.0.0"
INSTANCES_TABLE_HEADERS = ["UUID", "NAME", "ADB SERIAL", "STATE"]
UUID_HEADER_INDEX = INSTANCES_TABLE_HEADERS.index("UUID")


class InstanceState:
    """
    Possible state for Instances
    Note:
    - DELETED state is not part of the HTTP API but is still sent by push microservice.
    - UNKNOWN state is used internally when no state has been received yet.
    """

    # pylint: disable=too-few-public-methods
    UNKNOWN = "UNKNOWN"
    CREATING = "CREATING"
    OFFLINE = "OFFLINE"
    STARTING = "STARTING"
    BOOTING = "BOOTING"
    ONLINE = "ONLINE"
    SAVING = "SAVING"
    SAVED = "SAVED"
    STOPPING = "STOPPING"
    STOPPED = "STOPPED"
    DELETING = "DELETING"
    DELETED = "DELETED"
    MAINTENANCE = "MAINTENANCE"
    RECYCLED = "RECYCLED"
    ERROR = "ERROR"
    SAVING = "SAVING"


class TunnelState:
    """
    Possible states for AdbTunnel
    """

    # pylint: disable=too-few-public-methods
    DISCONNECTED = "DISCONNECTED"
    CONNECTED = "CONNECTED"
    PENDING = "PENDING"
    FAILED = "FAILED"
    PORT_BUSY = "PORT_BUSY"


def is_instance_starting(actual_state):
    """
    Return True if instance is neither started nor in failure, False otherwise.
    """
    return actual_state in [
        InstanceState.UNKNOWN,
        InstanceState.CREATING,
        InstanceState.OFFLINE,
        InstanceState.STARTING,
        InstanceState.BOOTING,
    ]


def is_instance_stopping(actual_state):
    """
    Return True if instance is neither stopped nor in failure, False otherwise.
    """
    return actual_state in [
        InstanceState.UNKNOWN,
        InstanceState.STOPPING,
        InstanceState.STOPPED,
        InstanceState.OFFLINE,
        InstanceState.DELETING,
    ]


def is_instance_saving(actual_state):
    """
    Return True if instance is neither stopped nor in failure, False otherwise.
    """
    return actual_state in [
        InstanceState.UNKNOWN,
        InstanceState.STOPPING,
        InstanceState.STOPPED,
        InstanceState.SAVING,
        InstanceState.SAVED,
        InstanceState.OFFLINE,
        InstanceState.DELETING,
    ]


def is_adbtunnel_connecting(actual_state):
    """
    Return True if instance is neither connected nor in failure, False otherwise.
    """
    return actual_state in [TunnelState.DISCONNECTED, TunnelState.PENDING]


class Instance:
    """
    Class representing one Instance with both API and ADB Tunnel information
    """

    def __init__(self, uuid=None):
        self.uuid = uuid or ""
        self.name = ""
        self.created_at = datetime.utcfromtimestamp(0).strftime("%Y-%m-%dT%H:%M:%S.000Z")
        self.max_run_duration = 0
        self.max_inactivity_duration = 0
        self.state = InstanceState.UNKNOWN
        self.tunnel_state = TunnelState.DISCONNECTED
        self._adb_serial = DEFAULT_ADB_SERIAL
        self.webrtc_url = ""
        self.recipe: Recipe = None

    def __str__(self):
        return "uuid={}, name={}, state={}, adb_serial={}, tunnel_state={}".format(
            self.uuid, self.name, self.state, self.adb_serial, self.tunnel_state
        )

    def as_dict(self):
        """Return Instance as a dict object
        Using OrderedDict here because dict() preserves insertion order since Python 3.7 only
        """
        data = OrderedDict()
        data["uuid"] = self.uuid
        data["name"] = self.name
        data["created_at"] = self.created_at
        data["max_run_duration"] = self.max_run_duration
        data["max_inactivity_duration"] = self.max_inactivity_duration
        data["state"] = self.state
        data["adbtunnel_state"] = self.tunnel_state
        data["adb_serial"] = self.adb_serial
        data["adb_serial_port"] = self.adb_serial_port or 0
        data["recipe"] = self.recipe.as_dict() if self.recipe else None
        return data

    @property
    def adb_serial(self):
        """Return adb_serial"""
        return self._adb_serial

    @adb_serial.setter
    def adb_serial(self, adb_serial):
        """Set adb_serial or set the default value"""
        if adb_serial:
            self._adb_serial = adb_serial
        else:
            self._adb_serial = DEFAULT_ADB_SERIAL

    @property
    def adb_serial_port(self):
        """
        Return port retrieved from ADB Serial, None on failure
        """
        try:
            return int([x for x in self.adb_serial.split(":") if x][1])
        except Exception:
            return None

    def set_state(self, state):
        """
        Update instance state and log change
        """
        LOGGER.debug("[%s] Update instance state from %s to %s", self.uuid, self.state, state)
        self.state = state

    @staticmethod
    def create_from_adbtunnel(raw_instance):
        """Factory function to get Instance object from ADB Tunnel content"""
        assert "uuid" in raw_instance
        assert "adb_serial" in raw_instance
        assert "state" in raw_instance
        instance = Instance()
        instance.uuid = raw_instance["uuid"]
        instance.adb_serial = raw_instance["adb_serial"]
        instance.tunnel_state = raw_instance["state"]
        return instance

    @staticmethod
    def create_from_saas(raw_instance):
        """Factory function to get Instance object from SaaS API content"""
        assert "uuid" in raw_instance
        assert "name" in raw_instance
        assert "created_at" in raw_instance
        assert "state" in raw_instance
        instance = Instance()
        instance.uuid = raw_instance["uuid"]
        instance.name = raw_instance["name"]
        instance.created_at = raw_instance["created_at"]
        instance.max_run_duration = raw_instance["timeouts"]["global"]
        instance.max_inactivity_duration = raw_instance["timeouts"]["inactivity"]
        instance.state = raw_instance["state"]
        instance.webrtc_url = raw_instance["webrtc_url"]
        if "recipe" in raw_instance:
            instance.recipe = Recipe.create_from_instance_endpoint(
                raw_instance.get("recipe"), raw_instance.get("hardware_profile"), raw_instance.get("os_image")
            )
        return instance

    @staticmethod
    def merge(saas_instance, adbtunnel_instance):
        """Merge Instance coming from ADB Tunnel into Instance coming from SaaS API"""
        merged_instance = saas_instance
        merged_instance.tunnel_state = adbtunnel_instance.tunnel_state
        merged_instance.adb_serial = adbtunnel_instance.adb_serial

        return merged_instance


class Instances:
    """Class storing a list of Instances"""

    def __init__(self):
        self.instances = []

    def __len__(self):
        return len(self.instances)

    def __iter__(self):
        return iter(self.instances)

    def as_list(self):
        """Return list of dict structured Instance"""
        self.sort()
        return [i.as_dict() for i in self.instances]

    @staticmethod
    def create_from_adbtunnel(raw_instances):
        """Factory function to get Instances object from ADB Tunnel content"""
        instances = Instances()
        for raw_instance in raw_instances:
            instances.instances.append(Instance.create_from_adbtunnel(raw_instance))
        return instances

    @staticmethod
    def create_from_saas(raw_instances):
        """Factory function to get Instances object from SaaS API content"""
        instances = Instances()
        instances.instances = [Instance.create_from_saas(raw_instance) for raw_instance in raw_instances]
        return instances

    @staticmethod
    def merge(saas_instances, adbtunnel_instances):
        """Merge Instances coming from ADB Tunnel into Instances coming from SaaS API"""
        merged_instances = saas_instances

        for merged_instance in merged_instances:
            for adbtunnel_instance in adbtunnel_instances:
                if merged_instance.uuid == adbtunnel_instance.uuid:
                    merged_instance.tunnel_state = adbtunnel_instance.tunnel_state
                    merged_instance.adb_serial = adbtunnel_instance.adb_serial

        return merged_instances

    def sort(self):
        """Sort instances in place by name"""
        self.instances = sorted(self.instances, key=lambda x: x.name)

    def get(self, instance_uuid, default_instance):
        """Return Instance for instance_uuid or default_instance if not found"""
        result = [i for i in self.instances if i.uuid == instance_uuid]
        if not result:
            return default_instance
        return result[0]

    def tabulate(self, quiet):
        """Return a tabulated string representation of instances"""
        self.sort()
        instances_table = self._get_table_format()

        if quiet:
            if instances_table:
                return "\n".join([x[UUID_HEADER_INDEX] for x in instances_table])
            return ""
        return tabulate(instances_table, headers=INSTANCES_TABLE_HEADERS, numalign="left")

    def _get_table_format(self):
        """
        Return instances as a two dimension table structure
        """
        formated_instances = [[i.uuid, i.name, i.adb_serial, i.state] for i in self.instances]
        return formated_instances
