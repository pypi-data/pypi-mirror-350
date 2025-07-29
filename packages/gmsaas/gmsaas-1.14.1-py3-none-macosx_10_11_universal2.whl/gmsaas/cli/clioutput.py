# Copyright 2020 Genymobile
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
gmsaas output controls
"""
from abc import ABC, abstractmethod
import json
from collections import OrderedDict
from typing import List

import click

from gmsaas.gmsaas.logger import LOGGER
from gmsaas.gmsaas.errors import ExitCode, DoctorCheck
from gmsaas.storage.configcache import get_output_format
from gmsaas.model.instanceinfo import Instances
from gmsaas.model.recipeinfo import Recipes
from gmsaas.model.osimageinfo import OsImages
from gmsaas.model.hwprofileinfo import HwProfiles

TEXT_OUTPUT = "text"
JSON_OUTPUT = "json"
COMPACT_JSON_OUTPUT = "compactjson"
OUTPUT_FORMATS = [TEXT_OUTPUT, JSON_OUTPUT, COMPACT_JSON_OUTPUT]


def ui():  # pylint: disable=invalid-name
    """Factory function returning the right Out instance"""
    output_format = OutputFormat.get()
    LOGGER.info("Using `%s` output format", output_format)
    if output_format == JSON_OUTPUT:
        return JSONOut()
    if output_format == COMPACT_JSON_OUTPUT:
        return CompactJSONOut()
    return PlainTextOut()


class OutputFormat:
    """Static class able to get the output format to use"""

    from_option = None

    @staticmethod
    def get():
        """Return the output format to use:
        * return format set with `--format` option if set
        * otherwise return format from configuration if set
        * else return the default format
        """
        output_format = OutputFormat.from_option
        if not output_format:
            output_format = get_output_format()
        if not output_format:
            output_format = TEXT_OUTPUT

        if output_format not in OUTPUT_FORMATS:
            LOGGER.warning("`%s` output format not supported, ignoring", output_format)
            return TEXT_OUTPUT

        return output_format


class Out(ABC):
    """Abstract class inherited by each output format supported"""

    def write_stdout(self, message, loggable=False):
        """Write message in stdout and log it if wanted"""
        if loggable:
            LOGGER.info(message)
        click.echo(message)

    def write_stderr(self, message, extra_log=None):
        """Write message in stderr, log it, also log `extra_log` if set"""
        LOGGER.error(message)
        if extra_log:
            LOGGER.error(extra_log)
        click.echo(message, err=True)

    @abstractmethod
    def error(self, exit_code, message, hint, details, extra_data=None, extra_message=None):
        """Output for any error raised by gmsaas"""

    @abstractmethod
    def show_version(self, name, version, doc_url, pypi_url):
        """Output for `gmsaas --version`"""

    @abstractmethod
    def auth_login(self, email, auth_cache_path):
        """Output for `gmsaas auth login`"""

    @abstractmethod
    def auth_token(self, auth_cache_path):
        """Output for `gmsaas auth token`"""

    @abstractmethod
    def auth_logout(self):
        """Output for `gmsaas auth logout`"""

    @abstractmethod
    def auth_reset(self):
        """Output for `gmsaas auth reset`"""

    @abstractmethod
    def auth_whoami(self, email, auth_cache_path):
        """Output for `gmsaas auth whoami`"""

    @abstractmethod
    def config_set(self, key, value):
        """Output for `gmsaas config set`"""

    @abstractmethod
    def config_get(self, key, value):
        """Output for `gmsaas config get`"""

    @abstractmethod
    def config_list(self, configuration):
        """Output for `gmsaas config list`"""

    @abstractmethod
    def instances_adbconnect(self, instance):
        """Output for `gmsaas instances adbconnect`"""

    @abstractmethod
    def instances_adbdisconnect(self, instance):
        """Output for `gmsaas instances adbdisconnect`"""

    @abstractmethod
    def instances_get(self, instance):
        """Output for `gmsaas instances get`"""

    @abstractmethod
    def instances_list(self, instances, quiet):
        """Output for `gmsaas instances list`"""

    @abstractmethod
    def instances_display(self, message):
        """Output for `gmsaas instances display`"""

    @abstractmethod
    def instances_start(self, instance):
        """Output for `gmsaas instances start`"""

    @abstractmethod
    def instances_save(self, instance):
        """Output for `gmsaas instances save`"""

    @abstractmethod
    def instances_saveas(self, instance, recipe_name, osimage_name):
        """Output for `gmsaas instances saveas`"""

    @abstractmethod
    def instances_stop(self, instance):
        """Output for `gmsaas instances stop`"""

    @abstractmethod
    def logzip(self, archive_path):
        """Output for `gmsaas logzip`"""

    @abstractmethod
    def recipes_create(self, recipe):
        """Output for `gmsaas recipes create`"""

    @abstractmethod
    def recipes_get(self, recipe):
        """Output for `gmsaas recipes get`"""

    @abstractmethod
    def recipes_list(self, recipes):
        """Output for `gmsaas recipes list`"""

    @abstractmethod
    def recipes_delete(self, recipe_uuid):
        """Output for `gmsaas recipes delete`"""

    @abstractmethod
    def osimages_create(self, osimage):
        """Output for `gmsaas osimages create`"""

    @abstractmethod
    def osimages_get(self, osimage):
        """Output for `gmsaas osimages get`"""

    @abstractmethod
    def osimages_list(self, osimages):
        """Output for `gmsaas osimages list`"""

    @abstractmethod
    def osimages_delete(self, osimage_uuid):
        """Output for `gmsaas osimages delete`"""

    @abstractmethod
    def hwprofiles_create(self, hwprofile):
        """Output for `gmsaas hwprofiles create`"""

    @abstractmethod
    def hwprofiles_get(self, hwprofile):
        """Output for `gmsaas hwprofile get`"""

    @abstractmethod
    def hwprofiles_list(self, hwprofiles):
        """Output for `gmsaas hwprofiles list`"""

    @abstractmethod
    def hwprofiles_delete(self, hwprofile_uuid):
        """Output for `gmsaas hwprofiles delete`"""

    @abstractmethod
    def doctor(self, checks_ok: List[DoctorCheck]):
        """Output for `gmsaas doctor`"""

    @abstractmethod
    def adb_start(self, adbtunnel_path, adb_path):
        """Output for `gmsaas adb start`"""

    @abstractmethod
    def adb_stop(self, adbtunnel_path, adb_path):
        """Output for `gmsaas adb stop`"""


class PlainTextOut(Out):
    """Subclass for text format output implementation"""

    def error(self, exit_code, message, hint, details, extra_data=None, extra_message=None):
        """Output for any error raised by gmsaas
        Note: `hint` is appended to message if it exists
        """
        del extra_data
        output = message
        if hint:
            output += "\n" + hint
        if extra_message:
            output += "\n" + extra_message
        self.write_stderr(output, details)

    def show_version(self, name, version, doc_url, pypi_url):
        """Output for `gmsaas --version`"""
        self.write_stdout("{} version {}\nDocumentation: {}\nChangelog: {}".format(name, version, doc_url, pypi_url))

    def auth_login(self, email, auth_cache_path):
        """Output for `gmsaas auth login`"""
        self.write_stdout(
            "User {} is logged in.\n" "Credentials saved to file: [{}]".format(email, auth_cache_path), loggable=True
        )

    def auth_token(self, auth_cache_path):
        """Output for `gmsaas auth token`"""
        self.write_stdout(f"API Token saved to file: [{auth_cache_path}]", loggable=True)

    def auth_logout(self):
        """Output for `gmsaas auth logout`"""
        self.write_stdout("Logged out.", loggable=True)

    def auth_reset(self):
        """Output for `gmsaas auth reset`"""
        self.write_stdout("Authentication cache cleared.", loggable=True)

    def auth_whoami(self, email, auth_cache_path):
        """Output for `gmsaas auth whoami`"""
        if email:
            self.write_stdout(email)
            return
        self.write_stdout("No credentials found. To set them up, use 'gmsaas auth login' command.")

    def config_set(self, key, value):
        """Output for `gmsaas config set`"""
        if not value:
            self.write_stdout("'{}' has been unset.".format(key))
            return
        self.write_stdout("'{}' has been set to '{}'.".format(key, value))

    def config_get(self, key, value):
        """Output for `gmsaas config get`"""
        self.write_stdout(value)

    def config_list(self, configuration):
        """Output for `gmsaas config list`"""
        items = sorted(["{}={}".format(key, configuration[key]) for key in configuration])
        self.write_stdout("\n".join(items))

    def instances_adbconnect(self, instance):
        """Output for `gmsaas instances adbconnect`"""
        self.write_stdout(instance.adb_serial)

    def instances_adbdisconnect(self, instance):
        """Output for `gmsaas instances adbdisconnect`"""

    def instances_get(self, instance):
        """Output for `gmsaas instances get`"""
        instances = Instances()
        instances.instances = [instance]
        self.instances_list(instances, False)

    def instances_list(self, instances, quiet):
        """Output for `gmsaas instances list`"""
        output = instances.tabulate(quiet)
        if output:
            self.write_stdout(output)

    def instances_display(self, message):
        """Output for `gmsaas instances display`"""
        self.write_stdout(message)

    def instances_start(self, instance):
        """Output for `gmsaas instances start`"""
        self.write_stdout(instance.uuid)

    def instances_save(self, instance):
        """Output for `gmsaas instances save`"""
        self.write_stdout(f"Instance '{instance.name}' has been saved successfully.")

    def instances_saveas(self, instance, recipe_name, osimage_name):
        """Output for `gmsaas instances saveas`"""
        self.write_stdout(
            f"Instance '{instance.name}' has been saved successfully. Recipe '{recipe_name}' and Image '{osimage_name}' have been created."
        )

    def instances_stop(self, instance):
        """Output for `gmsaas instances stop`"""

    def logzip(self, archive_path):
        """Output for `gmsaas logzip`"""
        self.write_stdout("'{}' generated.".format(archive_path))

    def recipes_create(self, recipe):
        """Output for `gmsaas recipes create`"""
        self.write_stdout(recipe.uuid)

    def recipes_get(self, recipe):
        """Output for `gmsaas recipes get`"""
        recipes = Recipes()
        recipes.recipes = [recipe]
        self.recipes_list(recipes)

    def recipes_list(self, recipes):
        """Output for `gmsaas recipes list`"""
        self.write_stdout(recipes.tabulate())

    def recipes_delete(self, recipe_uuid):
        """Output for `gmsaas recipes delete`"""
        self.write_stdout(f"Recipe '{recipe_uuid}' deleted successfully.")

    def osimages_create(self, osimage):
        """Output for `gmsaas osimages create`"""
        self.write_stdout(osimage.uuid)

    def osimages_get(self, osimage):
        """Output for `gmsaas osimages get`"""
        osimages = OsImages()
        osimages.osimages = [osimage]
        self.osimages_list(osimages)

    def osimages_list(self, osimages):
        """Output for `gmsaas osimages list`"""
        self.write_stdout(osimages.tabulate())

    def osimages_delete(self, osimage_uuid):
        """Output for `gmsaas osimages delete`"""
        self.write_stdout(f"Image '{osimage_uuid}' deleted successfully.")

    def hwprofiles_create(self, hwprofile):
        """Output for `gmsaas hwprofiles create`"""
        self.write_stdout(hwprofile.uuid)

    def hwprofiles_get(self, hwprofile):
        """Output for `gmsaas hwprofiles get`"""
        hwprofiles = HwProfiles()
        hwprofiles.hwprofiles = [hwprofile]
        self.hwprofiles_list(hwprofiles)

    def hwprofiles_list(self, hwprofiles):
        """Output for `gmsaas hwprofiles list`"""
        self.write_stdout(hwprofiles.tabulate())

    def hwprofiles_delete(self, hwprofile_uuid):
        """Output for `gmsaas hwprofiles delete`"""
        self.write_stdout(f"HwProfile '{hwprofile_uuid}' deleted successfully.")

    def doctor(self, checks_ok: List[DoctorCheck]):
        """Output for `gmsaas doctor`"""
        output = ["Check up finished:"]
        for check in checks_ok:
            if check == DoctorCheck.AUTH_CHECK:
                output.append("- Authentication OK.")
            if check == DoctorCheck.ADB_CHECK:
                output.append("- Android SDK OK.")
        self.write_stdout("\n".join(output))

    def adb_start(self, adbtunnel_path, adb_path):
        """Output for `gmsaas adb start`"""
        self.write_stdout(f"'{adbtunnel_path}' and '{adb_path}' started successfully.")

    def adb_stop(self, adbtunnel_path, adb_path):
        """Output for `gmsaas adb stop`"""
        self.write_stdout(f"'{adbtunnel_path}' and '{adb_path}' stopped successfully.")


class JSONOut(Out):
    """Subclass for JSON format output implementation"""

    def __init__(self, indent=4):
        self.indent = indent

    def write_data_stdout(self, data):
        """Add exit OK to data and print it as JSON"""
        data["exit_code"] = ExitCode.NO_ERROR.value
        data["exit_code_desc"] = ExitCode.NO_ERROR.name
        self.write_stdout(json.dumps(data, indent=self.indent, sort_keys=False))

    def write_data_stderr(self, data, exit_code):
        """Add exit code to data and print it as JSON"""
        data["exit_code"] = exit_code
        data["exit_code_desc"] = ExitCode(exit_code).name
        self.write_stderr(json.dumps(data, indent=self.indent, sort_keys=False))

    def error(self, exit_code, message, hint, details, extra_data=None, extra_message=None):
        """Output for any error raised by gmsaas
        Note: `hint` is not used in JSON output
        """
        del extra_message
        data = OrderedDict()
        data["error"] = {"message": message, "details": details or ""}
        if extra_data:
            data["error"].update(extra_data)
        self.write_data_stderr(data, exit_code)

    def show_version(self, name, version, doc_url, pypi_url):
        """Output for `gmsaas --version`"""
        data = OrderedDict()
        data["name"] = name
        data["version"] = version
        data["documentation_url"] = doc_url
        data["changelog_url"] = pypi_url
        self.write_data_stdout(data)

    def auth_login(self, email, auth_cache_path):
        """Output for `gmsaas auth login`"""
        data = OrderedDict()
        data["auth"] = OrderedDict([("email", email), ("credentials_path", auth_cache_path)])
        self.write_data_stdout(data)

    def auth_token(self, auth_cache_path):
        """Output for `gmsaas auth token`"""
        self.write_data_stdout({"auth": {"authentication_path": auth_cache_path}})

    def auth_logout(self):
        """Output for `gmsaas auth logout`"""
        self.write_data_stdout(OrderedDict())

    def auth_reset(self):
        """Output for `gmsaas auth reset`"""
        self.write_data_stdout(OrderedDict())

    def auth_whoami(self, email, auth_cache_path):
        """Output for `gmsaas auth whoami`"""
        self.auth_login(email, auth_cache_path)

    def config_set(self, key, value):
        """Output for `gmsaas config set`"""
        self.config_list({key: value})

    def config_get(self, key, value):
        """Output for `gmsaas config get`"""
        self.config_list({key: value})

    def config_list(self, configuration):
        """Output for `gmsaas config list`"""
        # configuration is {key: value} dict that need to be sorted
        data = OrderedDict(sorted(configuration.items(), key=lambda x: x[0]))
        self.write_data_stdout(OrderedDict([("configuration", data)]))

    def instances_adbconnect(self, instance):
        """Output for `gmsaas instances adbconnect`"""
        self.instances_start(instance)

    def instances_adbdisconnect(self, instance):
        """Output for `gmsaas instances adbdisconnect`"""
        self.instances_start(instance)

    def instances_get(self, instance):
        """Output for `gmsaas instances get`"""
        self.instances_start(instance)

    def instances_list(self, instances, quiet):
        """Output for `gmsaas instances list`"""
        self.write_data_stdout(OrderedDict([("instances", instances.as_list())]))

    def instances_display(self, message):
        """Output for `gmsaas instances display`"""
        self.write_data_stdout({"url": "<hidden>", "message": message})

    def instances_start(self, instance):
        """Output for `gmsaas instances start`"""
        self.write_data_stdout(OrderedDict([("instance", instance.as_dict())]))

    def instances_save(self, instance):
        """Output for `gmsaas instances save`"""
        self.write_data_stdout({"instance_uuid": instance.uuid})

    def instances_saveas(self, instance, recipe_name, osimage_name):
        """Output for `gmsaas instances saveas`"""
        self.write_data_stdout(
            {
                "instance_uuid": instance.uuid,
                "recipe_name": recipe_name,
                "osimage_name": osimage_name,
            }
        )

    def instances_stop(self, instance):
        """Output for `gmsaas instances stop`"""
        self.instances_start(instance)

    def logzip(self, archive_path):
        """Output for `gmsaas logzip`"""
        self.write_data_stdout(OrderedDict([("archive_path", archive_path)]))

    def recipes_create(self, recipe):
        """Output for `gmsaas recipes create`"""
        self.recipes_get(recipe)

    def recipes_get(self, recipe):
        """Output for `gmsaas recipes get`"""
        self.write_data_stdout({"recipe": recipe.as_dict()})

    def recipes_list(self, recipes):
        """Output for `gmsaas recipes list`"""
        self.write_data_stdout(OrderedDict([("recipes", recipes.as_list())]))

    def recipes_delete(self, recipe_uuid):
        """Output for `gmsaas recipes delete`"""
        self.write_data_stdout({"recipe_uuid": recipe_uuid})

    def osimages_create(self, osimage):
        """Output for `gmsaas osimages create`"""
        self.osimages_get(osimage)

    def osimages_get(self, osimage):
        """Output for `gmsaas osimages get`"""
        self.write_data_stdout({"osimage": osimage.as_dict()})

    def osimages_list(self, osimages):
        """Output for `gmsaas osimages list`"""
        self.write_data_stdout({"osimages": osimages.as_list()})

    def osimages_delete(self, osimage_uuid):
        """Output for `gmsaas osimages delete`"""
        self.write_data_stdout({"osimage_uuid": osimage_uuid})

    def hwprofiles_create(self, hwprofile):
        """Output for `gmsaas hwprofiles create`"""
        self.hwprofiles_get(hwprofile)

    def hwprofiles_get(self, hwprofile):
        """Output for `gmsaas hwprofiles get`"""
        self.write_data_stdout({"hwprofile": hwprofile.as_dict()})

    def hwprofiles_list(self, hwprofiles):
        """Output for `gmsaas hwprofiles list`"""
        self.write_data_stdout({"hwprofiles": hwprofiles.as_list()})

    def hwprofiles_delete(self, hwprofile_uuid):
        """Output for `gmsaas hwprofiles delete`"""
        self.write_data_stdout({"hwprofile_uuid": hwprofile_uuid})

    def doctor(self, checks_ok: List[DoctorCheck]):
        """Output for `gmsaas doctor`"""
        del checks_ok
        self.write_data_stdout({"issues": []})

    def adb_start(self, adbtunnel_path, adb_path):
        """Output for `gmsaas adb start`"""
        self.write_data_stdout(OrderedDict({"issues": []}))

    def adb_stop(self, adbtunnel_path, adb_path):
        """Output for `gmsaas adb stop`"""
        self.write_data_stdout(OrderedDict({"issues": []}))


class CompactJSONOut(JSONOut):
    """Subclass for compact JSON output implementation"""

    def __init__(self):
        super().__init__(indent=None)
