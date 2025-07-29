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
Cli for command adb
"""
import click
from gmsaas.cli.clioutput import ui
from gmsaas.adbtunnel import get_adbclient
from gmsaas.adbtunnel import get_adbtunnel
from gmsaas.cli.checks import auth_required, adb_tools_required
from gmsaas.gmsaas.logger import LOGGER


@click.group()
def adb():
    """
    ADB commands
    """


@click.command("stop", short_help="Stop both ADB and ADB Tunnel")
@click.pass_context
@auth_required
@adb_tools_required
def adb_stop(ctx):
    """
    Stop both ADB and ADB Tunnel
    """
    del ctx

    adbtunnel_client = get_adbtunnel()
    adbtunnel_client.stop()

    LOGGER.debug("Stopping ADB...")
    adb_client = get_adbclient()
    adb_client.stop()
    LOGGER.debug("ADB stopped.")

    ui().adb_stop(adbtunnel_client.exec_bin, adb_client.exec_bin)


@click.command("start", short_help="Start both ADB and ADB Tunnel")
@click.pass_context
@auth_required
@adb_tools_required
def adb_start(ctx):
    """
    Start both ADB and ADB Tunnel
    """
    del ctx

    LOGGER.debug("Starting ADB...")
    adb_client = get_adbclient()
    adb_client.start()
    LOGGER.debug("ADB started.")

    adbtunnel_client = get_adbtunnel()
    if not adbtunnel_client.start():
        LOGGER.error("ADB Tunnel not started in time")

    ui().adb_start(adbtunnel_client.exec_bin, adb_client.exec_bin)


adb.add_command(adb_start)
adb.add_command(adb_stop)
