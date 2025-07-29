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
Cli for subcommand auth
"""

import click

from gmsaas.saas import get_client
from gmsaas.storage import authcache
from gmsaas.adbtunnel import get_adbtunnel
from gmsaas.cli.clioutput import ui
from gmsaas.gmsaas.errors import ApiTokenNotSupportedError, CredentialsNotSupportedError
from gmsaas.cli.checks import print_credentials_deprecated


def _stop_adbtunnel():
    adbtunnel = get_adbtunnel()
    if adbtunnel.is_ready():
        adbtunnel.stop()


def _logout():
    _stop_adbtunnel()
    saas = get_client()
    saas.logout()
    authcache.clear()


def _auth_reset():
    _stop_adbtunnel()
    authcache.clear()


@click.group()
def auth():
    """
    Authentication commands
    """


@click.command(
    "token",
    help="Set an API Token for authentication. Not needed if `GENYMOTION_API_TOKEN` is set in your environment.",
)
@click.argument("token")
def auth_token(token: str) -> None:
    """
    Set an API Token for authentication.
    """
    # TODO GENYMOTION_API_TOKEN handling
    # TODO unittests
    authcache.clear()
    authcache.set_api_token(token)

    ui().auth_token(authcache.get_path())


@click.command(
    "login",
    help="<deprecated> Use `gmsaas auth token` instead. Authenticate with your credentials.",
)
@click.argument("email")
@click.argument("password", required=False)
def auth_login(email, password):
    """
    Authenticate with you credentials
    """
    # Note: `short_help` makes help text not being truncated to 45 char, don't remove it.

    print_credentials_deprecated()

    if not password:
        password = click.prompt("Password", type=click.STRING, hide_input=True)

    _logout()

    authcache.set_email(email)
    authcache.set_password(password)

    client = get_client()
    jwt = client.login()

    authcache.set_jwt(jwt)

    ui().auth_login(email, authcache.get_path())


@click.command("whoami", help="<deprecated> Display current authenticated user.")
def auth_whoami():
    """
    Display current authenticated user
    """
    if authcache.has_api_token():
        raise ApiTokenNotSupportedError()

    print_credentials_deprecated()
    ui().auth_whoami(authcache.get_email(), authcache.get_path())


@click.command("logout", help="<deprecated> Disconnect current user.")
def auth_logout():
    """
    Disconnect current user
    """
    if authcache.has_api_token():
        raise ApiTokenNotSupportedError("Use `gmsaas auth reset` instead.")
    print_credentials_deprecated()
    _logout()
    ui().auth_logout()


@click.command("reset", help="Clear API Token in cache if present.")
def auth_reset():
    """
    Clear API Token if stored locally
    """
    if not authcache.has_api_token() and authcache.has_credentials():
        raise CredentialsNotSupportedError("Use `gmsaas auth logout` instead.")
    _auth_reset()
    ui().auth_reset()


auth.add_command(auth_token)
auth.add_command(auth_login)
auth.add_command(auth_whoami)
auth.add_command(auth_logout)
auth.add_command(auth_reset)
