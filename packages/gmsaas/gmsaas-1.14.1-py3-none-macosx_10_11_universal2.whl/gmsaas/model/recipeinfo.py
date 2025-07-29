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
Recipe data
"""
from collections import OrderedDict

from packaging.version import parse
from tabulate import tabulate

from gmsaas.model.hwprofileinfo import HwProfile
from gmsaas.model.osimageinfo import OsImage
from gmsaas.utils.dictionnary import safe_get


RECIPES_TABLE_HEADERS = ["UUID", "NAME", "ANDROID", "SCREEN", "ARCH", "SOURCE"]
OFFICIAL_SOURCE = "genymotion"


def _key_for_entry(entry):
    source = entry.source
    is_official = entry.source == OFFICIAL_SOURCE
    version = entry.osimage.android_version if entry.osimage else "0.0.0"
    arch = entry.osimage.architecture if entry.osimage else ""
    name = entry.name
    version = parse(version)

    return (not is_official, source, version, arch, name)


class Recipe:
    """Class representing one Recipe"""

    def __init__(self, uuid=None):
        self.uuid = uuid or ""
        self.name = ""
        self.source = ""
        self.is_official: bool = None
        self.is_shared = False
        self.hwprofile: HwProfile = None
        self.osimage: OsImage = None

    def as_dict(self):
        """Return Recipe as dict object
        Using OrderedDict here because dict() preserves insertion order since Python 3.7 only
        """
        data = OrderedDict()
        data["uuid"] = self.uuid
        data["name"] = self.name
        data["android_version"] = self.osimage.android_version if self.osimage else "0.0.0"
        data["screen_width"] = self.hwprofile.screen_width if self.hwprofile else 0
        data["screen_height"] = self.hwprofile.screen_height if self.hwprofile else 0
        data["screen_density"] = self.hwprofile.screen_density if self.hwprofile else 0
        data["screen"] = self.hwprofile.screen if self.hwprofile else "Unknown"
        data["source"] = self.source
        data["hwprofile"] = self.hwprofile.as_dict() if self.hwprofile else None
        data["osimage"] = self.osimage.as_dict() if self.osimage else None
        return data

    @staticmethod
    def create_from_saas(raw_recipe):
        """Factory function to get Recipe object from SaaS API content"""
        if not raw_recipe:
            return None
        recipe = Recipe()
        recipe.uuid = raw_recipe["uuid"]
        recipe.name = raw_recipe["name"]
        recipe.source = OFFICIAL_SOURCE if raw_recipe["is_official"] else raw_recipe["owner"]["email"]
        recipe.is_official = raw_recipe["is_official"]
        recipe.is_shared = raw_recipe.get("share", None) is not None
        recipe.hwprofile = HwProfile.create_from_saas(raw_recipe["hardware_profile"])
        recipe.osimage = OsImage.create_from_saas(raw_recipe["os_image"])
        return recipe

    @staticmethod
    def create_from_instance_endpoint(raw_recipe, raw_hwprofile, raw_osimage):
        """Factory function to get Recipe object from SaaS API content
        Limitations:
        - does not provide share object
        """
        if raw_recipe is None:
            return None
        recipe = Recipe()
        recipe.uuid = raw_recipe["uuid"]
        recipe.name = raw_recipe["name"]
        recipe.source = OFFICIAL_SOURCE if not raw_recipe["owner"] else raw_recipe["owner"]["email"]
        recipe.is_shared = False  # TODO missing info from endpoint
        recipe.is_official = recipe.source == OFFICIAL_SOURCE
        # If hwprofile is not official, owner is the same than the recipe
        if raw_hwprofile and not safe_get(raw_hwprofile, "is_official", True):
            # If recipe has been deleted during instance run,
            # owner is null, in this edge case, owner is set to "Unknown"
            email = safe_get(raw_recipe, ["owner", "email"], "Unknown")
            raw_hwprofile["owner"] = {"email": email}
        # If osimage is not official, owner is the same than the recipe
        if raw_osimage and not safe_get(raw_osimage, "is_official", True):
            # If recipe has been deleted during instance run,
            # owner is null, in this edge case, owner is set to "Unknown"
            email = safe_get(raw_recipe, ["owner", "email"], "Unknown")
            raw_osimage["owner"] = {"email": email}
        recipe.hwprofile = HwProfile.create_from_instance_endpoint(raw_hwprofile)
        recipe.osimage = OsImage.create_from_saas(raw_osimage)
        return recipe


class Recipes:
    """Class storing a list of Recipe"""

    def __init__(self):
        self.recipes = []

    def __len__(self):
        return len(self.recipes)

    def __iter__(self):
        return iter(self.recipes)

    def as_list(self):
        """Return list of dict structured Recipe"""
        self.sort()
        return [r.as_dict() for r in self.recipes]

    @staticmethod
    def create_from_saas(raw_recipes):
        """Factory function to get Recipes object from SaaS API content"""
        recipes = Recipes()
        recipes.recipes = [Recipe.create_from_saas(raw_recipe) for raw_recipe in raw_recipes]
        return recipes

    def sort(self):
        """Sort recipes in place
        Recipes are sorted by several criteria which are (by priority ASC):
        NAME, ANDROID, SOURCE
        """
        self.recipes = sorted(self.recipes, key=_key_for_entry)

    def tabulate(self):
        """Return a tabulated string representation of recipes"""
        self.sort()
        recipes_table = self._get_table_format()
        return tabulate(recipes_table, headers=RECIPES_TABLE_HEADERS, numalign="left")

    def _get_table_format(self):
        """
        Return recipes as a two dimension table structure
        """
        formated_recipes = [
            [
                r.uuid,
                r.name,
                f"{r.osimage.android_version} {'[beta]' if r.osimage.is_beta else ''}" if r.osimage else "0.0.0",
                r.hwprofile.screen if r.hwprofile else "",
                r.osimage.architecture if r.osimage else "",
                r.source,
            ]
            for r in self.recipes
        ]
        return formated_recipes
