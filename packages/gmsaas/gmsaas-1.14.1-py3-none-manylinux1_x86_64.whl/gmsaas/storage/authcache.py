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
import os
from gmsaas.storage.crypto import cypher_v2, decypher_v1, decypher_v2
from gmsaas.storage import get_auth_storage
from gmsaas.storage.settings import get_gmsaas_auth_path
from gmsaas.gmsaas.logger import LOGGER


AUTH_EMAIL_KEY = "email"
AUTH_PASSWORD_KEY = "password"
AUTH_JWT_KEY = "jwt"
AUTH_API_TOKEN = "api_token"
AUTH_API_TOKEN_ENV = "GENYMOTION_API_TOKEN"


def get_path():
    """Return auth cache path"""
    return get_gmsaas_auth_path()


def get_email():
    """Return email from cache or None"""
    return PrivateAuthCache().get_email()


def get_password():
    """Return decoded password from cache or None"""
    return PrivateAuthCache().get_password()


def get_api_token():
    """Return API Token from cache or API Token from env or None"""
    api_token = PrivateAuthCache().get_api_token()
    api_token_from_env = os.environ.get(AUTH_API_TOKEN_ENV)
    if api_token and api_token_from_env:
        LOGGER.warning("API Token defined in cache and in environment, using cache")
    if not api_token and api_token_from_env:
        LOGGER.info("Using API Token defined from environment")
        api_token = api_token_from_env
    return api_token


def get_jwt():
    """Return jwt from cache or None"""
    return PrivateAuthCache().get_jwt()


def has_credentials():
    """Return True if email and password exist, False otherwise"""
    return PrivateAuthCache().get_email() is not None and PrivateAuthCache().get_password() is not None


def has_api_token() -> bool:
    """Return True if API Token exists, False otherwise"""
    return get_api_token() is not None


def set_email(email):
    """Save email in cache"""
    PrivateAuthCache().set_email(email)


def set_password(password):
    """Save encoded password in cache"""
    PrivateAuthCache().set_password(password)


def set_api_token(api_token):
    """Save api_token in cache"""
    PrivateAuthCache().set_api_token(api_token)


def set_jwt(jwt):
    """Save jwt and decoded token in cache"""
    PrivateAuthCache().set_jwt(jwt)


def clear():
    """Clear all cache entries"""
    PrivateAuthCache().clear()


class PrivateAuthCache:
    """
    Class that owns the auth storage and is in charge of data migration
    This class is private and should not be used directly
    """

    # pylint: disable=missing-docstring

    def __init__(self):
        self.storage = get_auth_storage()
        if self.storage.get_all() and self.storage.get_version() is None:
            # Meaning cache is not empty and is version 1
            # We need to migrate data in this case
            self._migrate_v1_to_v2()

    def _migrate_v1_to_v2(self):
        password = decypher_v1(self.storage.get(AUTH_PASSWORD_KEY))
        self.set_password(password)

    def get_email(self):
        return self.storage.get(AUTH_EMAIL_KEY)

    def get_password(self):
        password = self.storage.get(AUTH_PASSWORD_KEY)
        return decypher_v2(password)

    def get_jwt(self):
        return self.storage.get(AUTH_JWT_KEY)

    def get_api_token(self) -> str:
        return self.storage.get(AUTH_API_TOKEN)

    def set_email(self, email):
        self.storage.put(AUTH_EMAIL_KEY, email)

    def set_password(self, password):
        self.storage.put(AUTH_PASSWORD_KEY, cypher_v2(password))

    def set_jwt(self, jwt):
        self.storage.put(AUTH_JWT_KEY, jwt)

    def set_api_token(self, api_token: str) -> None:
        self.storage.put(AUTH_API_TOKEN, api_token)

    def clear(self):
        self.storage.clear()
