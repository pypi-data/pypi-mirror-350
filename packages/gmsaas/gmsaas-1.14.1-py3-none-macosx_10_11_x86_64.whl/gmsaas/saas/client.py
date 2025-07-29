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
Genymotion Cloud SaaS API client
"""

from abc import abstractmethod
import os
from urllib.parse import urlparse

import requests
from requests_toolbelt.utils import dump

import gmsaas

from gmsaas.gmsaas.triggererrors import get_fake_http_instance_state
from gmsaas.model.hwprofileinfo import HwProfiles, HwProfile
from gmsaas.storage import authcache
from gmsaas.gmsaas.proxy import get_proxies_from_config
from gmsaas.saas.sioclient import SIOClient, SocketIOUrl
from gmsaas.gmsaas import errors as err
from gmsaas.gmsaas.logger import LOGGER
from gmsaas.model.recipeinfo import Recipes, Recipe
from gmsaas.model.osimageinfo import OsImages, OsImage
from gmsaas.model.instanceinfo import (
    Instance,
    Instances,
    InstanceState,
    is_instance_starting,
    is_instance_stopping,
    is_instance_saving,
)
from gmsaas.saas.api import (
    get_hwprofiles_create_url,
    get_hwprofiles_get_url,
    get_hwprofiles_list_url,
    get_hwprofiles_delete_url,
    get_login_url,
    get_recipes_list_url,
    get_recipes_create_url,
    get_recipes_delete_url,
    get_instances_start_url,
    get_instances_stop_url,
    get_instances_save_url,
    get_instances_get_url,
    get_instances_list_url,
    get_logout_url,
    get_osimages_create_url,
    get_osimages_get_url,
    get_osimages_list_url,
    get_osimages_delete_url,
)
from gmsaas.gmsaas.timeout import wait_until, get_start_timeout, get_stop_timeout, get_save_timeout


HTTP_FAKE_INSTANCE_STATE = get_fake_http_instance_state()
SAVE_ACTION = "SAVE"
SAVE_AS_ACTION = "SAVE_AS"
ARCH_X86 = "x86"
ARCH_X86_64 = "x86_64"
ARCH_ARM_64 = "arm64"
SUPPORTED_ARCHS = [ARCH_X86, ARCH_X86_64, ARCH_ARM_64]


def _http_call(method, url, **kwargs):
    """
    Perform HTTP call and log around it
    """
    LOGGER.info("Request: %s %s", method.upper(), url)
    try:
        proxies = get_proxies_from_config()

        response = requests.request(method, url, proxies=proxies, timeout=30, **kwargs)
        if response:
            if LOGGER.verbosity > 1:
                response.request.body = "<hidden>"
                LOGGER.info("Response: %s", dump.dump_all(response).decode("utf-8"))
            else:
                LOGGER.info("Response: %s", response.status_code)
        else:
            # In case of error, request and response (including redirects) are logged.
            # Note: request's body is not logged as it can contain critical information.
            #       API Token is also hidden.
            response.request.body = "<hidden>"
            response.request.headers["x-api-token"] = "<hidden>"
            LOGGER.info("Response: %s", dump.dump_all(response).decode("utf-8"))
        return response
    except requests.exceptions.ProxyError as exception:
        raise err.ProxyError(exception) from exception
    except requests.exceptions.SSLError as exception:
        raise err.SSLError(exception) from exception
    except requests.RequestException as exception:
        # Possible exceptions http://docs.python-requests.org/en/latest/user/quickstart/#errors-and-exceptions
        # Despite the fact many causes can trigger exceptions, error message is oriented for ConnectionError.
        raise err.RequestError(exception) from exception


class AbstractClient:
    """
    Genymotion Cloud SaaS HTTP API client
    """

    SIO_BASE_URL = os.environ.get("GM_PLATFORM_SIO_BASE_URL", "https://ws.geny.io/cloud")

    def __init__(self):
        pass

    @staticmethod
    def _get_user_agent():
        """
        Craft User Agent HTTP header
        """

        user_agent_data = ["Genymobile", gmsaas.__application__, gmsaas.__version__]
        extra_data = os.environ.get("GMSAAS_USER_AGENT_EXTRA_DATA")
        if extra_data:
            user_agent_data.append(extra_data)
        return " ".join(user_agent_data)

    @abstractmethod
    def get_auth_header(self):
        """
        Return auth data to include in the request header
        """
        raise NotImplementedError()

    def _build_socketio_url(self, query_params) -> SocketIOUrl:
        """
        Return a SocketIOUrl named tuple for SocketIO connection

        Notes:
            SocketIO lib connection method takes two arguments:
                - url: base url (including query string params)
                - socketio_path: which is `socket.io` by default
            From our point of view:
                - url should be `https://ws.geny.io/cloud?token=...`
                - socketio_path: is right by default
            But the lib removes `/cloud` from our base url and so tries to connect to:
            `https://ws.geny.io/socket.io?token=...`.
            To counter that we need to deconstruct our base url in order to set in the lib:
                - url: `https://ws.geny.io?token=...`
                - socketio_path: cloud/socket.io
            This is what this method is doing.
        """
        base_url = urlparse(AbstractClient.SIO_BASE_URL)
        sio_base_url = "{}://{}{}".format(base_url.scheme, base_url.netloc, query_params)
        sio_path = base_url.path + "/socket.io"
        return SocketIOUrl(sio_base_url, sio_path)

    @abstractmethod
    def get_sio_url(self) -> SocketIOUrl:
        """
        Return an authenticated SIO URL
        """
        raise NotImplementedError()

    def _get_headers(self, auth_required=True):
        """
        Craft HTTP headers for request
        """
        headers = {
            "user-agent": self._get_user_agent(),
            "Content-Type": "application/json",
        }

        if auth_required:
            headers.update(self.get_auth_header())

        return headers

    @abstractmethod
    def make_api_call(self, api_call):
        """
        Wrap api call, can be overriden for specific logic
        """
        return api_call()

    def _get_paginated_results(self, url, ordering, page_size, **kwargs):
        """
        Perform HTTP calls on paginated endpoint, until all elements are fetched.
        Return results array.
        """
        count = None
        current_page = 1
        results = []

        while count is None or len(results) < count:
            params = {"page_size": page_size, "page": current_page}
            params.update(**kwargs)
            if ordering:
                params["ordering"] = ordering
            response = self.make_api_call(lambda: _http_call("get", url, headers=self._get_headers(), params=params))

            if response.status_code == 200:
                try:
                    data = response.json()
                    count = data["count"]
                    if not data["results"]:
                        # If results array is empty, early break here and so
                        # ignore the count property to avoid any infinite loop.
                        break
                    results.extend(data["results"])
                    current_page += 1
                except Exception as exception:
                    raise err.InvalidJsonError(response.status_code, response.text) from exception
            else:
                raise err.ApiError(response.status_code, response.text)

        return results

    def check_auth(self) -> bool:
        """
        Perform an authenticated webservice call to check the authentication
        Return True on success, False otherwise.
        Note: using GET instances for now, should use a dedicated endpoint in the future.
        """
        LOGGER.debug("Check authentication")
        try:
            response = self.make_api_call(
                lambda: _http_call("get", get_instances_list_url(), headers=self._get_headers())
            )
            return response.status_code == 200
        except Exception as error:
            LOGGER.error("Error while calling authenticated webservice:\n%s", str(error))
        return False

    def create_recipe(self, recipe_name, hwprofile_uuid, osimage_uuid, description):
        """
        Create custom recipe, return Recipe object
        """
        LOGGER.debug("Create Recipe %s from HwProfile %s and OsImage %s", recipe_name, hwprofile_uuid, osimage_uuid)

        payload = {"hardware_profile_uuid": hwprofile_uuid, "os_image_uuid": osimage_uuid, "name": recipe_name}
        if description:
            payload["description"] = description

        response = self.make_api_call(
            lambda: _http_call("post", get_recipes_create_url(), json=payload, headers=self._get_headers())
        )

        if response.status_code == 201:
            try:
                data = response.json()
                return Recipe.create_from_saas(data)
            except Exception as exception:
                raise err.InvalidJsonError(response.status_code, response.text) from exception
        else:
            raise err.ApiError(response.status_code, response.text)

    def get_recipe(self, recipe_uuid):
        """
        Get one Recipe
        Note: /v2/recipes/{uuid} does not return all information required
              to build correctly the Recipe object, hence the use of list endpoint
        """
        LOGGER.debug("Get Recipe %s", recipe_uuid)
        recipes = self.list_recipes(source="all", search=recipe_uuid)
        for recipe in recipes.recipes:
            if recipe.uuid == recipe_uuid:
                return recipe
        raise err.ApiError(404, "Recipe not found")

    def list_recipes(self, source, search=None):
        """
        List available Recipes for user, return Recipes object
        """
        LOGGER.debug("Listing available Recipes")
        results = self._get_paginated_results(
            get_recipes_list_url(), ordering=None, page_size=50, source=source, search=search, arch=SUPPORTED_ARCHS
        )
        return Recipes.create_from_saas(results)

    def delete_recipe(self, recipe_uuid, delete_osimage, delete_hwprofile):
        """
        Delete Recipe and (if wanted) associated OsImage / HwProfiles
        """
        LOGGER.debug(
            "Deleting Recipe %s, delete OsImage: %s, delete HwProfile %s", recipe_uuid, delete_osimage, delete_hwprofile
        )
        payload = {}
        if delete_osimage:
            payload["delete_hardware_profile"] = True
        if delete_hwprofile:
            payload["delete_os_image"] = True

        url = get_recipes_delete_url(recipe_uuid)

        response = self.make_api_call(lambda: _http_call("delete", url, json=payload, headers=self._get_headers()))
        if response.status_code == 204:
            return
        raise err.ApiError(response.status_code, response.text)

    def create_osimage(self, base_osimage_uuid, name):
        """
        Create a custom OsImage
        """
        LOGGER.debug("Creating OsImage %s from %s", name, base_osimage_uuid)
        payload = {"name": name}

        url = get_osimages_create_url(base_osimage_uuid)

        response = self.make_api_call(lambda: _http_call("post", url, json=payload, headers=self._get_headers()))

        if response.status_code == 201:
            try:
                data = response.json()
                return OsImage.create_from_saas(data)
            except Exception as exception:
                raise err.InvalidJsonError(response.status_code, response.text) from exception
        else:
            raise err.ApiError(response.status_code, response.text)

    def get_osimage(self, osimage_uuid):
        """
        Get one OsImage
        """
        LOGGER.debug("Get OsImage %s", osimage_uuid)

        url = get_osimages_get_url(osimage_uuid)

        response = self.make_api_call(lambda: _http_call("get", url, headers=self._get_headers()))

        if response.status_code == 200:
            try:
                data = response.json()
                return OsImage.create_from_saas(data)
            except Exception as exception:
                raise err.InvalidJsonError(response.status_code, response.text) from exception
        else:
            raise err.ApiError(response.status_code, response.text)

    def list_osimages(self):
        """
        List available OsImages for user, return Recipes object
        """
        LOGGER.debug("Listing available OsImages")
        results = self._get_paginated_results(
            get_osimages_list_url(), ordering=None, page_size=-1, arch=SUPPORTED_ARCHS
        )
        return OsImages.create_from_saas(results)

    def delete_osimage(self, osimage_uuid):
        """
        Delete OsImage
        """
        LOGGER.debug("Deleting OsImage %s", osimage_uuid)
        url = get_osimages_delete_url(osimage_uuid)

        response = self.make_api_call(lambda: _http_call("delete", url, headers=self._get_headers()))
        if response.status_code == 204:
            return
        raise err.ApiError(response.status_code, response.text)

    def create_hwprofile(
        self, name, width, height, density, navigation_bar, form_factor, cpu_count, ram_size, data_disk_size
    ):
        """
        Create a custom HwProfile
        """
        LOGGER.debug("Creating HwProfile %s", name)

        payload = {
            "name": name,
            "device_properties": {},
            "display_settings": {
                "displays": [{"width": width, "height": height, "density": density}],
                "hw_navigation_keys": not navigation_bar,
            },
            "form_factor": form_factor,
            "cpu_count": cpu_count,
            "ram_size": ram_size,
            "data_disk_size": data_disk_size,
        }

        url = get_hwprofiles_create_url()

        response = self.make_api_call(lambda: _http_call("post", url, json=payload, headers=self._get_headers()))

        if response.status_code == 201:
            try:
                data = response.json()
                return HwProfile.create_from_saas(data)
            except Exception as exception:
                raise err.InvalidJsonError(response.status_code, response.text) from exception
        else:
            raise err.ApiError(response.status_code, response.text)

    def get_hwprofile(self, hwprofile_uuid):
        """
        Get one HwProfile
        """
        LOGGER.debug("Get HwProfile %s", hwprofile_uuid)

        url = get_hwprofiles_get_url(hwprofile_uuid)

        response = self.make_api_call(lambda: _http_call("get", url, headers=self._get_headers()))

        if response.status_code == 200:
            try:
                data = response.json()
                return HwProfile.create_from_saas(data)
            except Exception as exception:
                raise err.InvalidJsonError(response.status_code, response.text) from exception
        else:
            raise err.ApiError(response.status_code, response.text)

    def list_hwprofiles(self):
        """
        List available HwProfiles for user, return HwProfiles object
        """
        LOGGER.debug("Listing available HwProfiles")
        results = self._get_paginated_results(get_hwprofiles_list_url(), ordering=None, page_size=50)
        return HwProfiles.create_from_saas(results)

    def delete_hwprofile(self, hwprofile_uuid):
        """
        Delete HwProfile
        """
        LOGGER.debug("Deleting HwProfile %s", hwprofile_uuid)
        url = get_hwprofiles_delete_url(hwprofile_uuid)

        response = self.make_api_call(lambda: _http_call("delete", url, headers=self._get_headers()))
        if response.status_code == 204:
            return
        raise err.ApiError(response.status_code, response.text)

    def get_instance(self, instance_uuid):
        """
        Return Instance from SaaS API
        """
        LOGGER.debug("Get instance")
        response = self.make_api_call(
            lambda: _http_call("get", get_instances_get_url(instance_uuid), headers=self._get_headers())
        )
        if response.status_code == 200:
            try:
                data = response.json()
                return Instance.create_from_saas(data)
            except Exception as exception:
                raise err.InvalidJsonError(response.status_code, response.text) from exception
        else:
            raise err.ApiError(response.status_code, response.text)

    def get_instances(self):
        """
        Return Instances from SaaS API
        """
        LOGGER.debug("Listing Instances")
        results = self._get_paginated_results(get_instances_list_url(), ordering="+created_at", page_size=50)
        return Instances.create_from_saas(results)

    def _request_instance_state(self, instance_uuid):
        """
        Return instance state via HTTP API
        """
        LOGGER.info("[%s] Request instance details", instance_uuid)

        if HTTP_FAKE_INSTANCE_STATE:
            LOGGER.info("Using fake instance state %s", HTTP_FAKE_INSTANCE_STATE)
            return HTTP_FAKE_INSTANCE_STATE

        url = get_instances_get_url(instance_uuid)
        response = self.make_api_call(lambda: _http_call("get", url, json={}, headers=self._get_headers()))

        if response.status_code in [200, 204]:
            try:
                return response.json()["state"]
            except Exception as exception:
                raise err.InvalidJsonError(response.status_code, response.text) from exception
        elif response.status_code == 404:
            LOGGER.info("[%s] Instance not found, considering it as DELETED", instance_uuid)
            return InstanceState.DELETED
        raise err.ApiError(response.status_code, response.text)

    def _wait_for_instance_stopped(self, instance_uuid):
        """
        Return the actual state whether it succeeds or not, the caller needs to check it.
        """
        LOGGER.debug("Waiting for %s stopped (HTTP fallback)", instance_uuid)
        wait_until(
            lambda: not is_instance_stopping(self._request_instance_state(instance_uuid)), get_stop_timeout(), period=3
        )
        return self._request_instance_state(instance_uuid)

    def _wait_for_instance_started(self, instance_uuid):
        """
        Return the actual state whether it succeeds or not, the caller needs to check it.
        """
        LOGGER.debug("Waiting for %s started (HTTP fallback)", instance_uuid)
        wait_until(
            lambda: not is_instance_starting(self._request_instance_state(instance_uuid)), get_start_timeout(), period=3
        )
        return self._request_instance_state(instance_uuid)

    def _wait_for_instance_saved(self, instance_uuid):
        """
        Return the actual state whether it succeeds or not, the caller needs to check it.
        """
        LOGGER.debug("Waiting for %s saved (HTTP fallback)", instance_uuid)
        wait_until(
            lambda: not is_instance_saving(self._request_instance_state(instance_uuid)), get_save_timeout(), period=3
        )
        return self._request_instance_state(instance_uuid)

    @abstractmethod
    def login(self):
        """
        Perform a login request
        """
        raise NotImplementedError()

    @abstractmethod
    def logout(self):
        """
        Perform a logout request
        """
        raise NotImplementedError()

    def _start_api_call(self, recipe_uuid, instance_name, timeout_params):
        """
        Start instance with API, returns dict response on success
        """
        payload = {"instance_name": instance_name}
        payload.update(timeout_params)
        url = get_instances_start_url(recipe_uuid)

        response = self.make_api_call(lambda: _http_call("post", url, json=payload, headers=self._get_headers()))
        if response.status_code == 201:
            try:
                return response.json()
            except Exception as exception:
                raise err.InvalidJsonError(response.status_code, response.text) from exception
        else:
            raise err.ApiError(response.status_code, response.text)

    def start_disposable_instance(self, recipe_uuid, instance_name, timeout_params, no_wait):
        """
        Start a new disposable instance, return Instance object
        """
        LOGGER.debug('Starting new "%s" disposable Instance', instance_name)

        instance = Instance.create_from_saas(self._start_api_call(recipe_uuid, instance_name, timeout_params))
        if no_wait:
            return instance

        with SIOClient(connection_url=self.get_sio_url()) as sio:
            if not sio.exception:
                instance.state = sio.wait_for_instance_started(instance.uuid)
            else:
                LOGGER.warning(
                    "[%s] SIO client unreachable (%s), fallback to HTTP polling", instance.uuid, str(sio.exception)
                )
            if is_instance_starting(instance.state):
                instance.state = self._wait_for_instance_started(instance.uuid)

        if is_instance_starting(instance.state):
            # Perform an HTTP call to be sure in case Socket.IO server got down,
            # or missed to push one message.
            LOGGER.info("[%s] Instance not started yet, perform HTTP request to confirm", instance.uuid)
            instance.state = self._request_instance_state(instance.uuid)

        if instance.state != InstanceState.ONLINE:
            LOGGER.error("[%s] Instance not started", instance.uuid)
            raise err.InstanceError(instance.uuid, InstanceState.ONLINE, instance.state)

        LOGGER.info("[%s] Instance started", instance.uuid)
        return instance

    def _stop_api_call(self, instance_uuid):
        """
        Stop instance with API returns dict response on success
        """
        url = get_instances_stop_url(instance_uuid)
        response = self.make_api_call(lambda: _http_call("post", url, json={}, headers=self._get_headers()))

        if response.status_code == 200:
            try:
                return response.json()
            except Exception as exception:
                raise err.InvalidJsonError(response.status_code, response.text) from exception
        else:
            raise err.ApiError(response.status_code, response.text)

    def stop_disposable_instance(self, instance_uuid, no_wait):
        """
        Stop a running disposable Instance, return Instance object
        """
        LOGGER.debug("[%s] Stopping disposable Instance", instance_uuid)

        instance = Instance.create_from_saas(self._stop_api_call(instance_uuid))
        if no_wait:
            return instance

        with SIOClient(connection_url=self.get_sio_url()) as sio:
            if not sio.exception:
                instance.state = sio.wait_for_instance_stopped(instance_uuid)
            else:
                LOGGER.warning(
                    "[%s] SIO client unreachable (%s), fallback to HTTP polling", instance.uuid, str(sio.exception)
                )
            if is_instance_stopping(instance.state):
                instance.state = self._wait_for_instance_stopped(instance_uuid)

        if is_instance_stopping(instance.state):
            # Perform an HTTP call to be sure in case Socket.IO server got down,
            # or missed to push one message.
            LOGGER.info("[%s] Instance not stopped yet, perform HTTP request to confirm", instance_uuid)
            instance.state = self._request_instance_state(instance_uuid)

        if instance.state != InstanceState.DELETED:
            LOGGER.error("[%s] Instance not stopped", instance_uuid)
            raise err.InstanceError(instance_uuid, InstanceState.DELETED, instance.state)

        LOGGER.info("[%s] Instance stopped", instance_uuid)
        return instance

    def _save_api_call(self, instance, action, recipe_name, osimage_name):
        """
        Save instance with API returns dict response on success
        """
        assert action in [SAVE_ACTION, SAVE_AS_ACTION]
        url = get_instances_save_url(instance.uuid)
        body = {"action": action}
        if recipe_name:
            body["new_recipe_name"] = recipe_name
        if osimage_name:
            body["new_os_image_name"] = osimage_name
        response = self.make_api_call(lambda: _http_call("post", url, json=body, headers=self._get_headers()))

        if response.status_code in [201, 204]:
            return
        if response.status_code == 400:
            raise err.SaveInstanceBadParamsError(
                f"Instance '{instance.name}' does not use a owned Recipe (or owned Image), please use 'saveas' command instead."
            )
        raise err.ApiError(response.status_code, response.text)

    def _save_instance(self, instance, action, recipe_name, osimage_name):
        self._save_api_call(instance, action, recipe_name, osimage_name)

        with SIOClient(connection_url=self.get_sio_url()) as sio:
            if not sio.exception:
                instance.state = sio.wait_for_instance_saved(instance.uuid)
            else:
                LOGGER.warning(
                    "[%s] SIO client unreachable (%s), fallback to HTTP polling", instance.uuid, str(sio.exception)
                )
                instance.state = self._request_instance_state(
                    instance.uuid
                )  # Refresh state because still ONLINE in cache.

            if is_instance_saving(instance.state):
                instance.state = self._wait_for_instance_saved(instance.uuid)

        if is_instance_saving(instance.state):
            # Perform an HTTP call to be sure in case Socket.IO server got down,
            # or missed to push one message.
            LOGGER.info("[%s] Instance not saved yet, perform HTTP request to confirm", instance.uuid)
            instance.state = self._request_instance_state(instance.uuid)

        if instance.state != InstanceState.DELETED:
            LOGGER.error("[%s] Instance not saved", instance.uuid)
            raise err.InstanceError(instance.uuid, InstanceState.DELETED, instance.state)

        LOGGER.info("[%s] Instance saved", instance.uuid)
        return instance

    def save_instance(self, instance):
        """
        Save a running disposable instance
        """
        LOGGER.debug("[%s] Saving Instance", instance.uuid)
        return self._save_instance(instance, SAVE_ACTION, recipe_name=None, osimage_name=None)

    def saveas_instance(self, instance, recipe_name, osimage_name):
        """
        Save as a running disposable instance
        """
        LOGGER.debug("[%s] Saving as Instance", instance.uuid)
        return self._save_instance(instance, SAVE_AS_ACTION, recipe_name, osimage_name)


class ApiTokenAuthClient(AbstractClient):
    """
    Perform API calls through API Token authentication
    """

    SIO_API_TOKEN_QUERY_STRING = "?api_token={}"

    def __init__(self, api_token: str):
        super().__init__()
        self.api_token: str = api_token

    @abstractmethod
    def logout(self):
        """
        Do nothing here
        """

    @abstractmethod
    def get_auth_header(self):
        """
        Return auth data to include in the request header
        """
        return {"x-api-token": self.api_token}

    @abstractmethod
    def get_sio_url(self) -> SocketIOUrl:
        """
        Return an authenticated SIO URL for API Token
        """
        return self._build_socketio_url(ApiTokenAuthClient.SIO_API_TOKEN_QUERY_STRING.format(self.api_token))


class CredentialsAuthClient(AbstractClient):
    """
    Perform API calls with credentials authentication
    """

    SIO_JWT_QUERY_STRING = "?token=Bearer%20{}"

    def __init__(self, email: str, password: str):
        super().__init__()
        self.email: str = email
        self.password: str = password
        self.jwt: str = None

    def _get_authorization(self):
        """
        Craft Authorization HTTP header for user
        """
        token = self._get_jwt()
        return "Bearer {}".format(token)

    @abstractmethod
    def get_auth_header(self):
        """
        Return auth data to include in the request header
        """
        return {"Authorization": self._get_authorization()}

    def make_api_call(self, api_call):
        response = api_call()
        if response.status_code == 401 or os.environ.get("GMSAAS_FORCE_JWT_REFRESH"):
            self._fetch_jwt()
            return api_call()
        return response

    def _get_jwt(self):
        """
        Get JWT for user
        """
        self.jwt = authcache.get_jwt()
        if not self.jwt:
            self._fetch_jwt()
        return self.jwt

    def _fetch_jwt(self):
        LOGGER.info("Requesting new JWT")
        payload = {"email": self.email, "password": self.password}
        response = _http_call("post", get_login_url(), json=payload, headers=self._get_headers(auth_required=False))
        if response.status_code == 200:
            try:
                self.jwt = response.json()["token"]
                authcache.set_jwt(self.jwt)
            except Exception as exception:
                raise err.AuthenticationError(response.status_code, response.text) from exception
        else:
            raise err.AuthenticationError(response.status_code, response.text)

    def get_sio_url(self) -> SocketIOUrl:
        """
        Return an authenticated SIO URL for JWT
        """
        return self._build_socketio_url(CredentialsAuthClient.SIO_JWT_QUERY_STRING.format(self._get_jwt()))

    def login(self):
        """
        Perform a login request
        """
        return self._get_jwt()

    def logout(self):
        """
        Call signout endpoint to trash the JWT properly on the platform
        """
        if not authcache.get_jwt():
            # No need to signout if no JWT present
            return

        url = get_logout_url()
        try:
            # Single shot call (retry is not required here)
            _http_call("post", url, headers=self._get_headers())
            LOGGER.info("Signed out from the platform")
        except Exception as exception:
            # Signout from the platform should not trigger any error
            LOGGER.warning("Cannot signout from the platform due to: %s", str(exception))
