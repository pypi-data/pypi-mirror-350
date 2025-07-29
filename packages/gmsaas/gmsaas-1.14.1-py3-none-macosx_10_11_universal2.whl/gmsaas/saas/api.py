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
Genymotion Cloud SaaS API constants
"""

import os

WEBSITE_URL = "https://cloud.geny.io"
CLOUD_BASE_URL = os.environ.get("GM_PLATFORM_BASE_URL", "https://api.geny.io/cloud")
LOGIN_URL = "{}/v1/users/login".format(CLOUD_BASE_URL)
LOGOUT_URL = "{}/v1/users/signout".format(CLOUD_BASE_URL)
RECIPES_V1_URL = "{}/v1/recipes".format(CLOUD_BASE_URL)
RECIPES_URL = "{}/v3/recipes/".format(CLOUD_BASE_URL)
INSTANCES_V1_URL = "{}/v1/instances".format(CLOUD_BASE_URL)
INSTANCES_V2_URL = "{}/v2/instances".format(CLOUD_BASE_URL)
OSIMAGES_URL = "{}/v1/os-images/".format(CLOUD_BASE_URL)
HWPROFILES_URL = "{}/v1/hardware-profiles/".format(CLOUD_BASE_URL)


def get_login_url():
    """
    Return URL to login
    """
    return LOGIN_URL


def get_logout_url():
    """
    Return URL to logout
    """
    return LOGOUT_URL


def get_recipes_list_url():
    """
    Return URL to get recipes
    """
    return RECIPES_URL


def get_recipes_create_url():
    """
    Return URL to create one recipe
    """
    return RECIPES_V1_URL


def get_recipes_delete_url(recipe_uuid: str):
    """
    Return URL to delete one recipe
    """
    return f"{RECIPES_V1_URL}/{recipe_uuid}"


def get_instances_start_url(recipe_uuid):
    """
    Return URL to start an instance
    """
    return f"{RECIPES_V1_URL}/{recipe_uuid}/start-disposable"


def get_instances_access_token_url():
    """
    Return URL to request a JWT allowed to access instances
    """
    return f"{INSTANCES_V1_URL}/access-token"


def get_instances_stop_url(instance_uuid):
    """
    Return URL to stop an instance
    """
    return f"{INSTANCES_V1_URL}/{instance_uuid}/stop-disposable"


def get_instances_save_url(instance_uuid):
    """
    Return URL to save an instance
    """
    return f"{INSTANCES_V1_URL}/{instance_uuid}/save"


def get_instances_get_url(instance_uuid):
    """
    Return URL to get details of one instance
    """
    return f"{INSTANCES_V1_URL}/{instance_uuid}"


def get_instances_list_url():
    """
    Return URL to get instances
    """
    return INSTANCES_V2_URL


def get_osimages_create_url(base_osimage_uuid):
    """
    Return URL to create one OsImage
    """
    return f"{OSIMAGES_URL}{base_osimage_uuid}/duplicate/"


def get_osimages_get_url(osimage_uuid):
    """
    Return URL to get one OsImage
    """
    return f"{OSIMAGES_URL}{osimage_uuid}"


def get_osimages_list_url():
    """
    Return URL to list OsImages
    """
    return OSIMAGES_URL


def get_osimages_delete_url(osimage_uuid):
    """
    Return URL to delete one OsImage
    """
    return f"{OSIMAGES_URL}{osimage_uuid}"


def get_hwprofiles_create_url():
    """
    Return URL to create one HwProfile
    """
    return HWPROFILES_URL


def get_hwprofiles_get_url(hwprofile_uuid):
    """
    Return URL to get one HwProfile
    """
    return f"{HWPROFILES_URL}{hwprofile_uuid}"


def get_hwprofiles_list_url():
    """
    Return URL to list HwProfiles
    """
    return HWPROFILES_URL


def get_hwprofiles_delete_url(hwprofile_uuid):
    """
    Return URL to delete one HwProfile
    """
    return f"{HWPROFILES_URL}{hwprofile_uuid}"
