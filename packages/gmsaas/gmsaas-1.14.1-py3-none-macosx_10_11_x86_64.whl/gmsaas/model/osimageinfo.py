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
OsImage model
"""
from packaging.version import parse

from tabulate import tabulate

from gmsaas.utils.dictionnary import safe_get


OSIMAGES_TABLE_HEADERS = ["UUID", "NAME", "ANDROID VERSION", "API VERSION", "ARCH", "SOURCE"]
UUID_HEADER_INDEX = OSIMAGES_TABLE_HEADERS.index("UUID")
UNKNOWN_PLACEHOLDER = "Unknown"


def _key_for_entry(entry):
    source = entry.source
    is_official = entry.source == "genymotion"
    version = parse(entry.android_version)
    arch = entry.architecture
    return (not is_official, source, version, arch)


class OsImage:
    """
    Class representing one OsImage coming from API
    """

    def __init__(self, uuid=None):
        self.uuid = uuid or ""
        self.name = ""
        self.image_version = "0.0.0"
        self.android_version = "0.0.0"
        self.api_version = 0
        self.architecture = ""
        self.source = ""
        self.is_official = None
        self.status = ""
        self.is_beta = False

    def __str__(self):
        return "uuid={}, name={}, image_version={}, android={}, api={}, arch={}, source={}".format(
            self.uuid,
            self.name,
            self.image_version,
            self.android_version,
            self.api_version,
            self.architecture,
            self.source,
        )

    def as_dict(self):
        """Return OsImage as a dict object"""
        data = {}
        data["uuid"] = self.uuid
        data["name"] = self.name
        data["image_version"] = self.image_version
        data["android_version"] = self.android_version
        data["api_version"] = self.api_version
        data["architecture"] = self.architecture
        data["source"] = self.source
        data["status"] = self.status
        data["is_beta"] = self.is_beta
        return data

    @staticmethod
    def create_from_saas(raw_osimage):
        """Factory function to get OsImage object from SaaS API content"""
        if not raw_osimage:
            return None
        osimage = OsImage()
        osimage.uuid = safe_get(raw_osimage, "uuid", "")
        osimage.name = safe_get(raw_osimage, "name", "")
        osimage.image_version = safe_get(raw_osimage, "image_version", "0.0.0")
        osimage.android_version = safe_get(raw_osimage, ["os_version", "os_version"], "0.0.0")
        osimage.api_version = safe_get(raw_osimage, ["os_version", "sdk_version"], 0)
        osimage.architecture = safe_get(raw_osimage, "arch", UNKNOWN_PLACEHOLDER)
        osimage.is_beta = safe_get(raw_osimage, "is_beta", False)
        is_official = safe_get(raw_osimage, "is_official", None)
        if is_official is None:
            osimage.source = UNKNOWN_PLACEHOLDER
        elif is_official:
            osimage.source = "genymotion"
            osimage.is_official = True
        else:
            osimage.source = safe_get(raw_osimage, ["owner", "email"], UNKNOWN_PLACEHOLDER)
        osimage.status = safe_get(raw_osimage, ["status"], UNKNOWN_PLACEHOLDER)

        return osimage


class OsImages:
    """Class storing a list of OsImages"""

    def __init__(self):
        self.osimages = []

    def __len__(self):
        return len(self.osimages)

    def __iter__(self):
        return iter(self.osimages)

    def as_list(self):
        """Return list of dict structured OsImages"""
        self.sort()
        return [i.as_dict() for i in self.osimages]

    @staticmethod
    def create_from_saas(raw_osimages):
        """Factory function to get OsImages object from SaaS API content"""
        osimages = OsImages()
        osimages.osimages = [OsImage.create_from_saas(raw_osimage) for raw_osimage in raw_osimages]
        return osimages

    def sort(self):
        """Sort instances in place by name"""
        self.osimages = sorted(self.osimages, key=_key_for_entry)

    def tabulate(self):
        """Return a tabulated string representation of instances"""
        self.sort()
        osimages_table = self._get_table_format()

        return tabulate(osimages_table, headers=OSIMAGES_TABLE_HEADERS, numalign="left")

    def _get_table_format(self):
        """
        Return instances as a two dimension table structure
        """
        formated_osimages = [
            [
                o.uuid,
                o.name,
                f"{o.android_version} {'[beta]' if o.is_beta else ''}",
                o.api_version,
                o.architecture,
                o.source,
            ]
            for o in self.osimages
        ]
        return formated_osimages
