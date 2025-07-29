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
Genymotion Cloud SaaS timeouts
"""

import os
import time


def wait_until(condition, timeout, period=1):
    """
    Wait until condition is met or expired timeout.
    Check period is 1 second.
    """
    must_end = time.time() + timeout
    while time.time() < must_end:
        if condition():
            return True
        time.sleep(period)
    return False


def get_start_timeout():
    """
    Return start timeout in seconds
    """
    return int(os.environ.get("GMSAAS_START_TIMEOUT", 300))


def get_stop_timeout():
    """
    Return stop timeout in seconds
    """
    return int(os.environ.get("GMSAAS_STOP_TIMEOUT", 120))


def get_save_timeout():
    """
    Return stop timeout in seconds
    """
    return int(os.environ.get("GMSAAS_SAVE_TIMEOUT", 900))


def get_adbconnect_timeout():
    """
    Return adbtunnel connection timeout in seconds
    """
    return int(os.environ.get("GMSAAS_ADBCONNECT_TIMEOUT", 60))


def get_adbdisconnect_timeout():
    """
    Return adbtunnel disconnection timeout in seconds
    """
    return int(os.environ.get("GMSAAS_ADBDISCONNECT_TIMEOUT", 30))


def get_adbtunnel_start_timeout():
    """
    Return adbtunnel start timeout in seconds
    """
    return int(os.environ.get("GMSAAS_ADBTUNNEL_START_TIMEOUT", 30))
