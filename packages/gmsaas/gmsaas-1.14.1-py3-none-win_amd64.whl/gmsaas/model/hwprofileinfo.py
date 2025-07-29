# Copyright 2023 Genymobile
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
HwProfile model
"""

from tabulate import tabulate
from gmsaas.utils.dictionnary import safe_get

HWPROFILES_TABLE_HEADERS = ["UUID", "NAME", "DISPLAY", "SOURCE"]
UUID_HEADER_INDEX = HWPROFILES_TABLE_HEADERS.index("UUID")
UNKNOWN_PLACEHOLDER = "Unknown"


def _key_for_entry(entry):
    is_official = entry.source == "genymotion"
    source = entry.source
    name = entry.name
    return (not is_official, source, name)


class HwProfile:
    """
    Class representing one HwProfile coming from API
    """

    def __init__(self, uuid=None):
        self.uuid = uuid or ""
        self.name = ""
        self.screen_width = 0
        self.screen_height = 0
        self.screen_density = 0
        self.hw_navigation_keys = False
        self.form_factor = None
        self.cpu_count = 0
        self.ram_size = 0
        self.data_disk_size = 0
        self.source = ""

    def __str__(self):
        return "uuid={}, name={}, source={}".format(
            self.uuid,
            self.name,
            self.source,
        )

    def as_dict(self):
        """Return HwProfile as a dict object"""
        data = {}
        data["uuid"] = self.uuid
        data["name"] = self.name
        data["form_factor"] = self.form_factor
        data["cpu_count"] = self.cpu_count
        data["ram_size"] = self.ram_size
        data["data_disk_size"] = self.data_disk_size
        data["source"] = self.source
        data["display_settings"] = {
            "hw_navigation_keys": self.hw_navigation_keys,
            "displays": [
                {
                    "width": self.screen_width,
                    "height": self.screen_height,
                    "density": self.screen_density,
                    "screen": self.screen,
                }
            ],
        }
        return data

    @property
    def screen(self):
        """Return string representation of screen properties"""
        if all([self.screen_width, self.screen_height, self.screen_density]):
            return "{} x {} dpi {}".format(self.screen_width, self.screen_height, self.screen_density)
        return UNKNOWN_PLACEHOLDER

    @staticmethod
    def create_from_saas(raw_hwprofile):
        """Factory function to get HwProfile object from SaaS API content"""
        if not raw_hwprofile:
            return None
        hwprofile = HwProfile()
        hwprofile.uuid = safe_get(raw_hwprofile, "uuid", "")
        hwprofile.name = safe_get(raw_hwprofile, "name", "")
        hwprofile.screen_width = safe_get(raw_hwprofile, ["display_settings", "displays", 0, "width"], 0)
        hwprofile.screen_height = safe_get(raw_hwprofile, ["display_settings", "displays", 0, "height"], 0)
        hwprofile.screen_density = safe_get(raw_hwprofile, ["display_settings", "displays", 0, "density"], 0)
        hwprofile.hw_navigation_keys = safe_get(raw_hwprofile, ["display_settings", "hw_navigation_keys"], None)
        hwprofile.form_factor = safe_get(raw_hwprofile, "form_factor", None)
        hwprofile.cpu_count = safe_get(raw_hwprofile, "cpu_count", 0)
        hwprofile.ram_size = safe_get(raw_hwprofile, "ram_size", 0)
        hwprofile.data_disk_size = safe_get(raw_hwprofile, "data_disk_size", 0)
        is_official = safe_get(raw_hwprofile, "is_official", None)
        if is_official is None:
            hwprofile.source = UNKNOWN_PLACEHOLDER
        elif is_official:
            hwprofile.source = "genymotion"
        else:
            hwprofile.source = safe_get(raw_hwprofile, ["owner", "email"], UNKNOWN_PLACEHOLDER)

        return hwprofile

    @staticmethod
    def create_from_instance_endpoint(raw_hwprofile):
        """Factory function to get HwProfile object from SaaS API content"""
        if not raw_hwprofile:
            return None
        hwprofile = HwProfile()
        hwprofile.uuid = safe_get(raw_hwprofile, "uuid", "")
        hwprofile.name = safe_get(raw_hwprofile, "name", "")
        hwprofile.screen_width = safe_get(raw_hwprofile, "width", 0)
        hwprofile.screen_height = safe_get(raw_hwprofile, "height", 0)
        hwprofile.screen_density = safe_get(raw_hwprofile, "density", 0)
        hwprofile.hw_navigation_keys = safe_get(raw_hwprofile, "hw_navigation_keys", None)
        hwprofile.form_factor = safe_get(raw_hwprofile, "form_factor", None)
        hwprofile.cpu_count = safe_get(raw_hwprofile, "cpu_count", 0)
        hwprofile.ram_size = safe_get(raw_hwprofile, "ram_size", 0)
        hwprofile.data_disk_size = safe_get(raw_hwprofile, "data_disk_size", 0)
        is_official = safe_get(raw_hwprofile, "is_official", None)
        if is_official is None:
            hwprofile.source = UNKNOWN_PLACEHOLDER
        elif is_official:
            hwprofile.source = "genymotion"
        else:
            hwprofile.source = safe_get(raw_hwprofile, ["owner", "email"], UNKNOWN_PLACEHOLDER)

        return hwprofile


class HwProfiles:
    """Class storing a list of HwProfiles"""

    def __init__(self):
        self.hwprofiles = []

    def __len__(self):
        return len(self.hwprofiles)

    def __iter__(self):
        return iter(self.hwprofiles)

    def as_list(self):
        """Return list of dict structured OsImages"""
        self.sort()
        return [i.as_dict() for i in self.hwprofiles]

    @staticmethod
    def create_from_saas(raw_hwprofiles):
        """Factory function to get OsImages object from SaaS API content"""
        hwprofiles = HwProfiles()
        hwprofiles.hwprofiles = [HwProfile.create_from_saas(raw_hwprofile) for raw_hwprofile in raw_hwprofiles]
        return hwprofiles

    def sort(self):
        """Sort instances in place by name"""
        self.hwprofiles = sorted(self.hwprofiles, key=_key_for_entry)

    def tabulate(self):
        """Return a tabulated string representation of instances"""
        self.sort()
        osimages_table = self._get_table_format()

        return tabulate(osimages_table, headers=HWPROFILES_TABLE_HEADERS, numalign="left")

    def _get_table_format(self):
        """
        Return instances as a two dimension table structure
        """
        formated_hwprofiles = [[hwp.uuid, hwp.name, hwp.screen, hwp.source] for hwp in self.hwprofiles]
        return formated_hwprofiles
