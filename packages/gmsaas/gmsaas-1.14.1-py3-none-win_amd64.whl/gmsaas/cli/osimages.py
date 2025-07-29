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
Cli for subcommand OsImages
"""
import click

from gmsaas.cli.checks import auth_required
from gmsaas.saas import get_client

from gmsaas.cli.clioutput import ui


@click.group("osimages")
def osimages_cmd_group():
    """
    Os Images commands
    """


@click.command("clone", help="Create a custom Image.")
@click.argument("BASE_OSIMAGE_UUID", type=click.UUID)
@click.argument("NAME", type=click.STRING)
@click.pass_context
@auth_required
def create_osimage(ctx, base_osimage_uuid, name):
    """
    Create a custom Image
    """
    del ctx
    base_osimage_uuid = str(base_osimage_uuid)
    saas = get_client()
    osimage = saas.create_osimage(base_osimage_uuid, name)
    ui().osimages_create(osimage)


@click.command("get", help="Get an Image details.")
@click.argument("OSIMAGE_UUID", type=click.UUID)
@click.pass_context
@auth_required
def get_osimage(ctx, osimage_uuid):
    """
    Get an Image details
    """
    del ctx
    saas = get_client()
    osimage = saas.get_osimage(osimage_uuid)
    ui().osimages_get(osimage)


@click.command("list", help="List all available Images.")
@click.pass_context
@auth_required
def list_osimages(ctx):
    """
    List all available Images
    """
    del ctx
    saas = get_client()
    osimages = saas.list_osimages()
    ui().osimages_list(osimages)


@click.command("delete", help="Delete an Image.")
@click.argument("OSIMAGE_UUID", type=click.UUID)
@click.pass_context
@auth_required
def delete_osimage(ctx, osimage_uuid):
    """
    Delete an Image
    """
    del ctx
    osimage_uuid = str(osimage_uuid)
    saas = get_client()
    saas.delete_osimage(osimage_uuid)
    ui().osimages_delete(osimage_uuid)


osimages_cmd_group.add_command(create_osimage)
osimages_cmd_group.add_command(get_osimage)
osimages_cmd_group.add_command(list_osimages)
osimages_cmd_group.add_command(delete_osimage)
