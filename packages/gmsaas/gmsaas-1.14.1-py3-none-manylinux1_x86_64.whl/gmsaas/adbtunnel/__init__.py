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
ADB tunnel binary wrapper
"""
import platform

try:
    # For Python 3.9 and above
    from importlib.resources import files
except ImportError:
    # For Python 3.8 and below, use the backport
    from importlib_resources import files

from gmsaas.adbtunnel.adbtunnelclient import AdbTunnelClient
from gmsaas.adbtunnel.adbclient import AdbClient
from gmsaas.storage.configcache import get_android_sdk_path


def get_adbtunnel_dir():
    """Get gmadbtunneld dir"""
    return files(__name__) / "gmadbtunneld"


def get_adbtunnel():
    """Get AdbTunnelClient instance"""
    system = platform.system()
    is_windows = system == "Windows"
    is_macos = system == "Darwin"

    gmadbtunneld_dir = get_adbtunnel_dir()

    adbtunneld_exec = gmadbtunneld_dir / "gmadbtunneld"
    if is_windows:
        adbtunneld_exec = gmadbtunneld_dir / "gmadbtunneld.exe"
    elif is_macos:
        adbtunneld_exec = gmadbtunneld_dir / "gmadbtunneld.app/Contents/MacOS/gmadbtunneld"

    return AdbTunnelClient(adbtunneld_exec)


def get_adbclient():
    """Get AdbClient instance"""
    return AdbClient(get_android_sdk_path())
