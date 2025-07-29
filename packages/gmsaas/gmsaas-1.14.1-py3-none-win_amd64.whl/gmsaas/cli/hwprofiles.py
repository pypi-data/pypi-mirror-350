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
Cli for subcommand HwProfiles
"""
import click

from gmsaas.cli.checks import auth_required
from gmsaas.saas import get_client

from gmsaas.gmsaas.logger import LOGGER
from gmsaas.cli.clioutput import ui


@click.group("hwprofiles")
def hwprofiles_cmd_group():
    """
    Hardware Profiles commands
    """


@click.command("create", help="Create a custom Hardware Profile.")
@click.argument("NAME", type=click.STRING)
@click.option(
    "--width",
    type=click.IntRange(240, 7680),
    default=768,
    show_default=True,
    help="Display width in pixels.",
)
@click.option(
    "--height",
    type=click.IntRange(240, 7680),
    default=1280,
    show_default=True,
    help="Display height in pixels.",
)
@click.option(
    "--density",
    type=click.IntRange(80, 820),
    default=320,
    show_default=True,
    help="Display density in pixels per inch.",
)
@click.option(
    "--navigation-bar",
    type=click.BOOL,
    is_flag=True,
    help="If set, display the Android navigation bar.",
)
@click.option(
    "--form-factor",
    type=click.Choice(["PHONE", "TABLET"]),
    default="PHONE",
    show_default=True,
    help="Form factor.",
)
@click.pass_context
@auth_required
def create_hwprofile(ctx, name, width, height, density, navigation_bar, form_factor):
    """
    Create a custom Hardware Profile
    """
    del ctx
    saas = get_client()

    # These values are consistents with the default values used by the frontend.
    # For now we don't expose the customization of theses values through gmsaas.
    cpu_count = 2
    ram_size = 2048
    data_disk_size = 16384

    hwprofile = saas.create_hwprofile(
        name, width, height, density, navigation_bar, form_factor, cpu_count, ram_size, data_disk_size
    )
    ui().hwprofiles_create(hwprofile)


@click.command("get", help="Get a Hardware Profile details.")
@click.argument("HWPROFILE_UUID", type=click.UUID)
@click.pass_context
@auth_required
def get_hwprofile(ctx, hwprofile_uuid):
    """
    Get a Hardware Profile details
    """
    del ctx
    hwprofile_uuid = str(hwprofile_uuid)
    saas = get_client()
    hwprofile = saas.get_hwprofile(hwprofile_uuid)
    ui().hwprofiles_get(hwprofile)


@click.command("list", help="List all available Hardware Profiles.")
@click.pass_context
@auth_required
def list_hwprofiles(ctx):
    """
    List all available Hardware Profiles
    """
    del ctx
    saas = get_client()
    hwprofiles = saas.list_hwprofiles()

    LOGGER.debug("%d HwProfiles available", len(hwprofiles))

    ui().hwprofiles_list(hwprofiles)


@click.command("delete", help="Delete a Hardware Profile.")
@click.argument("HWPROFILE_UUID", type=click.UUID)
@click.pass_context
@auth_required
def delete_hwprofile(ctx, hwprofile_uuid):
    """
    Delete a Hardware Profile
    """
    del ctx
    hwprofile_uuid = str(hwprofile_uuid)
    saas = get_client()
    saas.delete_hwprofile(hwprofile_uuid)
    ui().hwprofiles_delete(hwprofile_uuid)


hwprofiles_cmd_group.add_command(create_hwprofile)
hwprofiles_cmd_group.add_command(get_hwprofile)
hwprofiles_cmd_group.add_command(list_hwprofiles)
hwprofiles_cmd_group.add_command(delete_hwprofile)
