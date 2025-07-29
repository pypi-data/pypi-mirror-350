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
""" gmsaas package """
import os

__application__ = "gmsaas"
__version__ = os.environ.get("GMSAAS_VERSION", "1.14.1")


def get_name():
    """Return gmsaas application name"""
    return __application__


def get_version():
    """Return gmsaas version string"""
    return __version__


def get_doc_url():
    """Return documentation URL for current gmsaas version"""
    version = get_version()
    return "https://docs.genymotion.com/gmsaas/{}.x/".format(version[0])


def get_pypi_url():
    """Return PyPI URL for current gmsaas version"""
    return "https://pypi.org/project/gmsaas/{}/".format(get_version())
