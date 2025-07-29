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
""" Access to data storage """

import stat

from gmsaas.storage.settings import get_gmsaas_auth_path, get_gmsaas_config_path
from gmsaas.storage.json_file_storage import JsonFileStorage


CONFIG_STORAGE_VERSION = 1
AUTH_STORAGE_VERSION = 2


def get_config_storage():
    """Get configuration storage implementation"""
    return JsonFileStorage(get_gmsaas_config_path(), CONFIG_STORAGE_VERSION)


def get_auth_storage():
    """Get auth storage implementation"""
    return JsonFileStorage(get_gmsaas_auth_path(), AUTH_STORAGE_VERSION, stat.S_IRUSR | stat.S_IWUSR)
