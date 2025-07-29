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
Configuration file
"""

import os
import sys

try:
    # For Python 3.9 and above
    from importlib.resources import files
except ImportError:
    # For Python 3.8 and below, use the backport
    from importlib_resources import files

import click

import gmsaas

TMP_DIR_NAME = "tmp"


def _get_genymobile_config_home_path():
    """
    Return path of Genymobile config home, default is `~/.Genymobile`
    """
    if sys.platform.startswith("win32"):
        home_path = "%LOCALAPPDATA%\\Genymobile"
    else:
        home_path = os.path.expanduser("$HOME/.Genymobile")
    home_path = os.path.expanduser(os.path.expandvars(home_path))
    return home_path


def get_gmsaas_config_home_path():
    """
    Return path of gmsaas config home, default is `~/.Genymobile/gmsaas`
    Raise exception if folder is not correct
    """
    config_home = os.path.join(_get_genymobile_config_home_path(), gmsaas.__application__)
    if "GMSAAS_CONFIG_HOME" in os.environ:
        config_home = os.path.expanduser(os.environ["GMSAAS_CONFIG_HOME"])
        if not config_home:
            raise click.ClickException("Error: GMSAAS_CONFIG_HOME is set but empty")
        if not os.path.isabs(config_home):
            raise click.ClickException("Error: GMSAAS_CONFIG_HOME '{}' must be an absolute path.".format(config_home))
    try:
        os.makedirs(os.path.join(config_home, TMP_DIR_NAME), exist_ok=True)  # Create deepest dir.
    except Exception as error:
        raise click.ClickException(
            "Error: cannot create gmsaas config home located at '{}' ({})".format(config_home, str(error))
        )
    return config_home


def get_gmsaas_auth_path():
    """
    Return path of auth.json
    """
    return os.path.join(get_gmsaas_config_home_path(), "auth.json")


def get_gmsaas_config_path():
    """
    Return path of config.json
    """
    return os.path.join(get_gmsaas_config_home_path(), "config.json")


def get_gmsaas_assets_path():
    """
    Return path where assets files are stored.
    """
    return files("gmsaas") / "assets"


def get_gmsaas_log_path():
    """
    Return path of gmsaas.log
    """
    return os.path.join(get_gmsaas_config_home_path(), "gmsaas.log")


def get_gmadbtunneld_log_path():
    """
    Return path of gmadbtunneld.log
    """
    return os.path.join(get_gmsaas_config_home_path(), "gmadbtunneld.log")


def get_tmp_path():
    """
    Return path where tmp files can be stored
    """
    return os.path.join(get_gmsaas_config_home_path(), TMP_DIR_NAME)
