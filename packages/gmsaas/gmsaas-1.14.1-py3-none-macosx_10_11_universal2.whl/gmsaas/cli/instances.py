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
Cli for subcommand instance
"""
import os
import shutil
import sys
from pathlib import Path
from urllib.parse import urlencode

import click
import pyperclip

from gmsaas.model.instanceinfo import Instance, Instances, InstanceState, TunnelState, is_instance_starting
from gmsaas.gmsaas import errors as err
from gmsaas.cli.checks import auth_required, adb_tools_required
from gmsaas.saas import get_client
from gmsaas.adbtunnel import get_adbtunnel
from gmsaas.gmsaas.logger import LOGGER, log_elapsed_time
from gmsaas.cli.clioutput import ui
from gmsaas.saas.api import CLOUD_BASE_URL
from gmsaas.storage.settings import get_gmsaas_assets_path


@click.group("instances")
def instances_cmd_group():
    """
    Instances commands
    """


@click.command("start", short_help="Start an Instance.", help="Start an Instance from a Recipe.")
@click.argument("RECIPE_UUID", type=click.UUID)
@click.argument("INSTANCE_NAME")
@click.option(
    "--stop-when-inactive",
    type=click.BOOL,
    is_flag=True,
    help="<deprecated> Use '--max-run-duration' instead. If set, the Instance will be stopped if no web app interactions are made for a certain duration, this duration is the organization's default inactivity timeout.",
)
@click.option(
    "--max-run-duration",
    type=click.IntRange(0, 28800),
    help="Duration in minute after which the Instance will be stopped, no matter what. The countdown starts when Instance is booted. 0 means no timeout. By default the organization's default global timeout is used.",
)
@click.option("--no-wait", type=click.BOOL, is_flag=True, help="Do not wait for the Instance to be fully started.")
@click.pass_context
@auth_required
@log_elapsed_time
def start_disposable_instance(ctx, recipe_uuid, instance_name, stop_when_inactive, max_run_duration, no_wait):
    """
    Start an instance from a Recipe
    """
    del ctx
    saas = _get_api_client()

    if stop_when_inactive and max_run_duration is not None:
        raise click.BadParameter("Options '--stop-when-inactive' and '--max-run-duration' are mutally exclusives.")

    timeout_params = {}
    if stop_when_inactive:
        timeout_params["stop_when_inactive"] = True
    else:
        # gmsaas always disables the inactivity timeout (relevant from webapp, not from cmd line)
        timeout_params["timeouts"] = {"inactivity": 0}
        if isinstance(max_run_duration, int):
            # Override organization's global timeout if set
            timeout_params["timeouts"].update({"global": max_run_duration})

    instance = saas.start_disposable_instance(recipe_uuid, instance_name, timeout_params, no_wait)
    ui().instances_start(instance)


@click.command(
    "save",
    short_help="Save a running Instance.",
    help="Save running Instance using owned Recipe/Image, Instance will stop in order to be saved.",
)
@click.argument("INSTANCE_UUID", type=click.UUID)
@click.pass_context
@auth_required
@log_elapsed_time
def save_instance(ctx, instance_uuid):
    """
    Save running Instance using owned Recipe/Image, Instance will stop in order to be saved.
    """
    del ctx
    instance_uuid = str(instance_uuid)

    saas = _get_api_client()

    instance = saas.get_instance(instance_uuid)

    if instance.recipe.is_official:
        raise err.SaveInstanceBadParamsError(
            f"Instance '{instance.name}' does not use a owned Recipe, please use 'saveas' command instead."
        )
    if instance.recipe.osimage.is_official:
        raise err.SaveInstanceBadParamsError(
            f"Instance '{instance.name}' does not use an owned Image, please use 'saveas' command instead."
        )

    if instance.state != InstanceState.ONLINE:
        raise err.SaveInstanceBadParamsError(f"Instance '{instance.name}' is not ready to be saved.")

    adbtunnel = get_adbtunnel()
    adbtunnel.disconnect(instance_uuid)
    tunnel_state = adbtunnel.wait_for_adb_disconnected(instance_uuid).tunnel_state
    if tunnel_state != TunnelState.DISCONNECTED:
        LOGGER.error("[%s] Instance can't be disconnected from ADB tunnel", instance_uuid)
    saas = _get_api_client()
    saas.save_instance(instance)
    ui().instances_save(instance)


SAVEAS_HELP = """
\b
Save running Instance in a new owned Recipe/Image, Instance will stop in order to be saved.
Note: you can not "Save As" a Recipe owned by another organization.
"""


@click.command("saveas", short_help="Save As a running Instance.", help=SAVEAS_HELP)
@click.argument("INSTANCE_UUID", type=click.UUID)
@click.option(
    "--osimage-name",
    type=click.STRING,
    required=True,
    help="Name for saved Image.",
)
@click.option(
    "--recipe-name",
    type=click.STRING,
    required=True,
    help="Name for saved Recipe.",
)
@click.pass_context
@auth_required
@log_elapsed_time
def saveas_instance(ctx, instance_uuid, recipe_name, osimage_name):
    """
    Save running instance in a new owned Recipe/Image.
    """
    del ctx
    instance_uuid = str(instance_uuid)

    saas = _get_api_client()

    instance = saas.get_instance(instance_uuid)

    if instance.state != InstanceState.ONLINE:
        raise err.SaveInstanceBadParamsError(f"Instance '{instance.name}' is not ready to be saved.")

    adbtunnel = get_adbtunnel()
    adbtunnel.disconnect(instance_uuid)
    tunnel_state = adbtunnel.wait_for_adb_disconnected(instance_uuid).tunnel_state
    if tunnel_state != TunnelState.DISCONNECTED:
        LOGGER.error("[%s] Instance can't be disconnected from ADB tunnel", instance_uuid)
    saas = _get_api_client()
    saas.saveas_instance(instance, recipe_name, osimage_name)
    ui().instances_saveas(instance, recipe_name, osimage_name)


@click.command("stop", short_help="Stop a running Instance.")
@click.argument("INSTANCE_UUID", type=click.UUID)
@click.option("--no-wait", type=click.BOOL, is_flag=True, help="Do not wait for the Instance to be fully stopped.")
@click.pass_context
@auth_required
@adb_tools_required
@log_elapsed_time
def stop_disposable_instance(ctx, instance_uuid, no_wait):
    """
    Stop a running disposable instance
    """
    del ctx
    instance_uuid = str(instance_uuid)
    adbtunnel = get_adbtunnel()
    adbtunnel.disconnect(instance_uuid)
    tunnel_state = adbtunnel.wait_for_adb_disconnected(instance_uuid).tunnel_state
    if tunnel_state != TunnelState.DISCONNECTED:
        LOGGER.error("[%s] Instance can't be disconnected from ADB tunnel", instance_uuid)
    saas = _get_api_client()
    instance = saas.stop_disposable_instance(instance_uuid, no_wait)
    ui().instances_stop(instance)


@click.command("get", short_help="Get a running Instance.")
@click.argument("INSTANCE_UUID", type=click.UUID)
@click.pass_context
@auth_required
@adb_tools_required
@log_elapsed_time
def get_instance(ctx, instance_uuid):
    """
    Get instance information
    """
    del ctx
    instance_uuid = str(instance_uuid)
    saas = _get_api_client()
    adbtunnel = get_adbtunnel()
    saas_instance = saas.get_instance(instance_uuid)
    adbtunnel_instance = adbtunnel.get_instance(instance_uuid)
    instance = Instance.merge(saas_instance, adbtunnel_instance)

    ui().instances_get(instance)


@click.command("list", short_help="List running Instances.")
@click.option("--quiet", "-q", is_flag=True, help="Only display running Instance UUIDs.")
@click.pass_context
@auth_required
@adb_tools_required
@log_elapsed_time
def list_instances(ctx, quiet):
    """
    List all currently running instances
    """
    del ctx
    saas = _get_api_client()
    adbtunnel = get_adbtunnel()
    saas_instances = saas.get_instances()
    adbtunnel_instances = adbtunnel.get_instances()
    instances = Instances.merge(saas_instances, adbtunnel_instances)

    LOGGER.debug("%d Instances available", len(instances))
    ui().instances_list(instances, quiet)


@click.command("adbconnect", short_help="Connect ADB to a running Instance.")
@click.option("--adb-serial-port", type=click.IntRange(1024, 65535))
@click.argument("INSTANCE_UUID", type=click.UUID)
@click.pass_context
@auth_required
@adb_tools_required
@log_elapsed_time
def connect_instance_to_adb(ctx, instance_uuid, adb_serial_port):
    """
    Connect a running instance to ADB
    """
    del ctx
    instance_uuid = str(instance_uuid)

    saas = _get_api_client()
    adbtunnel = get_adbtunnel()
    saas_instance = saas.get_instance(instance_uuid)
    adbtunnel_instance = adbtunnel.get_instance(instance_uuid)
    instance = Instance.merge(saas_instance, adbtunnel_instance)

    if instance.state != InstanceState.ONLINE:
        # Instance should be started in order to connect ADB
        raise err.AdbTunnelInstanceNotReadyError(instance_uuid, instance.state)

    running_port = instance.adb_serial_port
    if running_port:
        # ADB Tunnel is already running for this instance
        # If it's on the same port: early return
        # Else raise an error
        if running_port == adb_serial_port or not adb_serial_port:
            LOGGER.info("[%s] Instance already connected to ADB tunnel", instance_uuid)
            ui().instances_adbconnect(instance)
            return
        raise err.AdbTunnelRunningOnDifferentPortError(instance_uuid, running_port, adb_serial_port)

    adbtunnel.connect(instance_uuid, adb_serial_port)
    adbtunnel_instance = adbtunnel.wait_for_adb_connected(instance_uuid)
    instance = Instance.merge(instance, adbtunnel_instance)

    if instance.tunnel_state == TunnelState.CONNECTED:
        LOGGER.info("[%s] Instance connected to ADB tunnel", instance_uuid)
        ui().instances_adbconnect(instance)
        return
    if instance.tunnel_state == TunnelState.PORT_BUSY:
        raise err.AdbTunnelBusyPortError(instance_uuid, adb_serial_port)
    # Consider the operation timed out
    adbtunnel.disconnect(instance_uuid)
    adbtunnel.wait_for_adb_disconnected(instance_uuid)
    raise err.AdbTunnelConnectTimeoutError(instance_uuid)


@click.command("adbdisconnect", short_help="Disconnect ADB from a running Instance.")
@click.argument("INSTANCE_UUID", type=click.UUID)
@click.pass_context
@auth_required
@adb_tools_required
@log_elapsed_time
def disconnect_instance_from_adb(ctx, instance_uuid):
    """
    Disconnect a running instance from ADB
    """
    del ctx
    instance_uuid = str(instance_uuid)

    saas = _get_api_client()
    adbtunnel = get_adbtunnel()
    saas_instance = saas.get_instance(instance_uuid)
    adbtunnel_instance = adbtunnel.get_instance(instance_uuid)
    instance = Instance.merge(saas_instance, adbtunnel_instance)

    adbtunnel.disconnect(instance_uuid)
    adbtunnel_instance = adbtunnel.wait_for_adb_disconnected(instance_uuid)
    instance = Instance.merge(instance, adbtunnel_instance)

    if instance.tunnel_state == TunnelState.DISCONNECTED:
        LOGGER.info("[%s] Instance disconnected from ADB tunnel", instance_uuid)
        ui().instances_adbdisconnect(instance)
        return
    raise err.AdbTunnelDisonnectTimeoutError(instance_uuid)


DISPLAY_SHORT_HELP = "Display instances locally in gmsaas portal."

DEFAULT_GMSAAS_DISPLAY_LIMIT = 30


def _get_gmsaas_display_limit():
    return int(os.environ.get("GMSAAS_DISPLAY_LIMIT", DEFAULT_GMSAAS_DISPLAY_LIMIT))


def _prepare_portal_path():
    """
    :return: the path to the html portal file
    If env var GMSAAS_PORTAL_DIR is set, return this path, otherwise:

    For Windows/macOS: return the html portal file directly from embedded gmsaas assets.

    For Linux:

    Preliminary note:
    `snap` (which is a wide spread Linux package manager) installs apps in a sandbox which:
    1. Deny access to hidden files
    2. Sandboxed default /tmp dir

    If the web browser has been installed through snap, it will not have access to:
    1. gmsaas assets folder (as gmsaas is installed in hidden dir `.local`)
    2. gmsaas config home folder (as located in hidden dir `.Genymobile`)
    3. Standard `/tmp` dir

    To workaround that, on Linux we:
    1. Copy the portal assets in `~/gmsaas.tmp` dir
    2. Use this location to create the portal URL
    """

    def _get_portal_path(portal_dir):
        return os.path.normpath(os.path.join(portal_dir, "portal.html"))

    portal_dir = os.environ.get("GMSAAS_PORTAL_DIR")
    if portal_dir:
        if os.path.isfile(os.path.join(portal_dir, "portal.html")):
            return _get_portal_path(portal_dir)
        raise err.DisplayInstanceError(f"Unable to find `portal.html` in {portal_dir}")

    assets_path = get_gmsaas_assets_path()

    if sys.platform in ["win32", "darwin"]:
        return _get_portal_path(assets_path)

    tmp_dir = os.path.join(Path.home(), "gmsaas.tmp")

    try:
        os.makedirs(tmp_dir, exist_ok=True)
    except Exception as error:
        raise err.DisplayInstanceError(f"Unable to create tmp dir in {tmp_dir}: {error}")

    try:
        shutil.copytree(src=get_gmsaas_assets_path(), dst=tmp_dir, dirs_exist_ok=True)
    except Exception as error:
        raise err.DisplayInstanceError(f"Unable to prepare gmsaas portal in {tmp_dir}: {error}")
    return _get_portal_path(tmp_dir)


@click.command(
    "display",
    short_help=DISPLAY_SHORT_HELP,
    help=f"{DISPLAY_SHORT_HELP} ({DEFAULT_GMSAAS_DISPLAY_LIMIT} instances max.)",
)
@click.option("--yes", "-y", is_flag=True, help="Accept to copy sensitive data in clipboard.")
@click.argument("INSTANCE_UUID", type=click.UUID, required=False, nargs=-1)
@click.pass_context
@auth_required
@adb_tools_required
@log_elapsed_time
def display_instance(ctx, instance_uuid, yes):
    """
    Display instance
    """
    del ctx

    saas = _get_api_client()
    if not instance_uuid:
        instances = saas.get_instances()
        instance_uuids = [
            str(x.uuid) for x in instances if (is_instance_starting(x.state) or x.state == InstanceState.ONLINE)
        ]
    else:
        instance_uuids = [str(x) for x in instance_uuid]

    if not instance_uuids:
        raise err.DisplayInstanceError("No running instances to display.")

    if not yes:
        if not click.confirm("Sensitive data (authentication token) will be copied in your clipboard, continue?"):
            raise err.DisplayInstanceError("Aborted operation.")

    message = "Generated URL copied in your clipboard, paste it in your web browser."
    max_display_instances = _get_gmsaas_display_limit()
    if max_display_instances and len(instance_uuids) > max_display_instances:
        message += f"\n(i) Number of instances has been limited to {max_display_instances} for a better experience."
        instance_uuids = instance_uuids[0:max_display_instances]

    params = [("instances[]", uuid) for uuid in instance_uuids]

    # Pass the authentication header needed to call SaaS apis.
    auth_header = saas.get_auth_header()
    auth_header_key = list(auth_header.keys())[0]
    params.append(("auth_header_key", auth_header_key))  # ex: "Authorization"
    params.append(("auth_header_value", auth_header[auth_header_key]))  # ex: "Bearer <jwt>"

    if "staging" in CLOUD_BASE_URL:
        params.append(("url", CLOUD_BASE_URL))
    encoded_params = urlencode(params)

    html_path = _prepare_portal_path()
    url = f"file://{html_path}?{encoded_params}"

    try:
        pyperclip.copy(url)
    except pyperclip.PyperclipException as exc:
        raise err.DisplayInstanceError(
            "Unable to copy the url to the clipboard. An additional package may be required. "
            "See https://pyperclip.readthedocs.io/en/latest/index.html#not-implemented-error"
        ) from exc
    ui().instances_display(message)


def _get_api_client():
    """
    Get the Genymotion Cloud SaaS API client
    """
    return get_client()


instances_cmd_group.add_command(start_disposable_instance)
instances_cmd_group.add_command(save_instance)
instances_cmd_group.add_command(saveas_instance)
instances_cmd_group.add_command(stop_disposable_instance)
instances_cmd_group.add_command(get_instance)
instances_cmd_group.add_command(list_instances)
instances_cmd_group.add_command(connect_instance_to_adb)
instances_cmd_group.add_command(disconnect_instance_from_adb)
instances_cmd_group.add_command(display_instance)
