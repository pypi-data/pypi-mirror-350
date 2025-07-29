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
gmsaas trigger errors
"""
import os


def _get_errors():
    return [x for x in os.environ.get("GMSAAS_TRIGGER_ERRORS", "").split(",") if x]


def _contains_error(error):
    return error in _get_errors()


def _get_fake_value(key):
    for error in _get_errors():
        items = error.split("{}=".format(key))
        if len(items) == 2:
            return items[1]
    return None


def trigger_sio_unreachable():
    """
    Return True if unreachable sio should be triggered, False otherwise
    """
    return _contains_error("sio_unreachable")


def get_fake_sio_instance_state():
    """
    Return instance state to use for sio, None otherwise
    """
    return _get_fake_value("sio_instance_state")


def get_fake_http_instance_state():
    """
    Return instance state to use for http, None otherwise
    """
    return _get_fake_value("http_instance_state")


def trigger_unrecognized_state():
    """
    Return True if unrecognized instance state should be triggered, False otherwise
    """
    return _contains_error("unrecognized_instance_state")


def get_fake_adbtunnel_state():
    """
    Return adbtunnel state to use, None otherwise
    """
    return _get_fake_value("adbtunnel_state")
