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
Cli for subcommand recipes
"""
import click

from gmsaas.cli.checks import auth_required
from gmsaas.saas import get_client

from gmsaas.gmsaas.logger import LOGGER
from gmsaas.cli.clioutput import ui


@click.group("recipes")
def recipes_cmd_group():
    """
    Recipes commands
    """


@click.command("create", help="Create a custom Recipe.")
@click.argument("HWPROFILE_UUID", type=click.UUID)
@click.argument("OSIMAGE_UUID", type=click.UUID)
@click.argument("RECIPE_NAME")
@click.option(
    "--description",
    type=click.STRING,
    help="Description text for this Recipe.",
)
@click.pass_context
@auth_required
def create_recipe(ctx, hwprofile_uuid, osimage_uuid, recipe_name, description):
    """
    Create a custom Recipe
    """
    del ctx
    hwprofile_uuid = str(hwprofile_uuid)
    osimage_uuid = str(osimage_uuid)

    saas = get_client()

    recipe = saas.create_recipe(recipe_name, hwprofile_uuid, osimage_uuid, description)
    ui().recipes_create(recipe)


@click.command("get", help="Get a Recipe details.")
@click.argument("RECIPE_UUID", type=click.UUID)
@click.pass_context
@auth_required
def get_recipe(ctx, recipe_uuid):
    """
    Get a Recipe details
    """
    del ctx
    recipe_uuid = str(recipe_uuid)
    saas = get_client()
    recipe = saas.get_recipe(recipe_uuid)
    ui().recipes_get(recipe)


@click.command("list", help="List available Recipes.")
@click.option("--name", help="Filter results with substring.")
@click.option("--source", type=click.Choice(["all", "official", "custom"]), default="all", show_default=True)
@click.pass_context
@auth_required
def list_recipes(ctx, name, source):
    """
    List available Recipes
    """
    del ctx
    if source == "custom":
        source = "shared"
    saas = get_client()
    recipes = saas.list_recipes(source=source, search=name)

    LOGGER.debug("%d Recipes available", len(recipes))

    ui().recipes_list(recipes)


@click.command("delete", help="Delete a Recipe.")
@click.argument("RECIPE_UUID", type=click.UUID)
@click.option(
    "--delete-osimage",
    type=click.BOOL,
    is_flag=True,
    help="If set, the associated Image is deleted too.",
)
@click.option(
    "--delete-hwprofile",
    type=click.BOOL,
    is_flag=True,
    help="If set, the associated Hardware Profile is deleted too.",
)
@click.pass_context
@auth_required
def delete_recipe(ctx, recipe_uuid, delete_osimage, delete_hwprofile):
    """
    Delete a Recipe
    """
    del ctx
    recipe_uuid = str(recipe_uuid)
    saas = get_client()
    saas.delete_recipe(recipe_uuid, delete_osimage, delete_hwprofile)
    ui().recipes_delete(recipe_uuid)


recipes_cmd_group.add_command(create_recipe)
recipes_cmd_group.add_command(get_recipe)
recipes_cmd_group.add_command(list_recipes)
recipes_cmd_group.add_command(delete_recipe)
