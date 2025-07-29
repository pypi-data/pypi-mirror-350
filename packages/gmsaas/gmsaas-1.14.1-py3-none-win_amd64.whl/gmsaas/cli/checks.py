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
gmsaas early checks
"""
import click
import gmsaas
from gmsaas.gmsaas.proxy import get_proxy_info
from gmsaas.storage import authcache
from gmsaas.saas.api import CLOUD_BASE_URL, WEBSITE_URL
from gmsaas.gmsaas import errors as err
from gmsaas.adbtunnel import get_adbtunnel, get_adbclient
from gmsaas.cli.clioutput import OutputFormat, TEXT_OUTPUT


DEPRECATED_CREDENTIALS = f"***\n* Using credentials to authenticate is deprecated.\n* Please create an API Token on {WEBSITE_URL}/api and use `gmsaas auth token` in order to authenticate.\n***"


def print_credentials_deprecated():
    """
    Print a warning in stdout suggesting user to use API Token.
    This function only prints the warning in TEXT format in order
    to not break JSON parsing.
    TODO: rework this part to add the warning in JSON output too.
    """
    if OutputFormat.get() == TEXT_OUTPUT:
        click.echo(DEPRECATED_CREDENTIALS, err=True)


def auth_required(func):
    """
    Check if an api_token or email/password credentials are stored locally
    """

    def wrapper(self, *args, **kwargs):
        # pylint: disable=missing-docstring
        has_api_token = authcache.has_api_token()
        has_credentials = authcache.has_credentials()
        if not has_api_token and not has_credentials:
            raise err.NoAuthenticationError()
        if has_credentials:
            print_credentials_deprecated()
        func(self, *args, **kwargs)

    return wrapper


def _get_major_minor(major_minor_patch_version):
    return ".".join(major_minor_patch_version.split(".")[:2])


def adb_tools_required(func):
    """
    Check if android sdk path is stored locally
    and adbtunnel is usable
    """

    def wrapper(self, *args, **kwargs):
        # pylint: disable=missing-docstring
        adbclient = get_adbclient()
        if not adbclient.is_ready():
            raise err.NoAndroidToolsError()
        adbtunnel = get_adbtunnel()
        if not adbtunnel.is_ready():
            raise err.PackageError(adbtunnel.exec_bin)
        daemon_info = adbtunnel.get_daemon_info()
        if _get_major_minor(gmsaas.__version__) != _get_major_minor(daemon_info.version):
            raise err.MismatchedVersionError(gmsaas.__version__, daemon_info.version)
        if CLOUD_BASE_URL != daemon_info.platform_url:
            raise err.MismatchedPlatformUrlError(CLOUD_BASE_URL, daemon_info.platform_url)
        if get_proxy_info() != daemon_info.proxy:
            raise err.MismatchedProxyError(get_proxy_info(), daemon_info.proxy)
        func(self, *args, **kwargs)

    return wrapper
