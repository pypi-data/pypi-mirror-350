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
Genymotion Cloud SaaS auth cache functions
"""
from gmsaas.storage import get_config_storage


SDK_PATH_KEY = "android-sdk-path"
PROXY_KEY = "proxy"
OUTPUT_FORMAT_KEY = "output-format"


def get_config(key):
    """Return config value of key or "" """
    return get_config_storage().get(key) or ""


def get_all():
    """Return all config values, password is decoded"""
    return get_config_storage().get_all()


def get_android_sdk_path():
    """Return Android SDK path from cache or "" """
    return get_config_storage().get(SDK_PATH_KEY) or ""


def get_proxy_url():
    """Return proxy from cache or "" """
    return get_config_storage().get(PROXY_KEY) or ""


def get_output_format():
    """Return output format from cache or "" """
    return get_config_storage().get(OUTPUT_FORMAT_KEY) or ""


def set_config(key, value):
    """Save key/value in cache"""
    get_config_storage().put(key, value)


def set_android_sdk_path(sdk_path):
    """Save Android SDK path in cache"""
    set_config(SDK_PATH_KEY, sdk_path)


def set_proxy_url(proxy_url):
    """Save proxy host in cache"""
    set_config(PROXY_KEY, proxy_url)


def set_output_format(output_format):
    """Save output format in cache"""
    set_config(OUTPUT_FORMAT_KEY, output_format)
