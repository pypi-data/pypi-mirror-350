# Copyright 2024 Genymobile
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
Cli for command doctor
"""
from typing import List
import click
from gmsaas.cli.clioutput import ui
from gmsaas.saas import get_client
from gmsaas.adbtunnel import get_adbclient
from gmsaas.gmsaas.errors import DoctorError, DoctorCheck


@click.command("doctor")
@click.option(
    "--auth",
    required=False,
    is_flag=True,
    help="Check gmsaas authentication",
)
@click.option(
    "--adb",
    required=False,
    is_flag=True,
    help="Check ADB configuration",
)
@click.pass_context
def doctor(ctx, adb, auth):
    """
    Check if gmsaas is correctly configured
    """
    del ctx

    check_adb = adb
    check_auth = auth

    if not check_adb and not check_auth:
        check_adb = True
        check_auth = True

    checks_ok: List[DoctorCheck] = []
    checks_ko: List[DoctorCheck] = []

    if check_auth:
        try:
            saas = get_client()
            check_ok = saas.check_auth()
            if check_ok:
                checks_ok.append(DoctorCheck.AUTH_CHECK)
            else:
                checks_ko.append(DoctorCheck.AUTH_CHECK)
        except Exception:
            checks_ko.append(DoctorCheck.AUTH_CHECK)

    if check_adb:
        adbclient = get_adbclient()
        if adbclient.is_ready():
            checks_ok.append(DoctorCheck.ADB_CHECK)
        else:
            checks_ko.append(DoctorCheck.ADB_CHECK)

    if len(checks_ko) > 0:
        raise DoctorError(checks_ko)

    ui().doctor(checks_ok)
