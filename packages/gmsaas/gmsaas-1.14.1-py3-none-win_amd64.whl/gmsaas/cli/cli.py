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
gmsaas entry point
"""

import sys

import click

import gmsaas
from gmsaas.cli.clioutput import ui
from gmsaas.cli.auth import auth
from gmsaas.cli.config import config
from gmsaas.cli.hwprofiles import hwprofiles_cmd_group
from gmsaas.storage.configcache import PROXY_KEY
from gmsaas.cli.recipes import recipes_cmd_group
from gmsaas.cli.osimages import osimages_cmd_group
from gmsaas.cli.instances import instances_cmd_group
from gmsaas.cli.logzip import logzip
from gmsaas.cli.doctor import doctor
from gmsaas.cli.adb import adb
from gmsaas.gmsaas.logger import set_verbosity, LOGGER
from gmsaas.gmsaas.proxy import setup_proxy
from gmsaas.cli.clioutput import OutputFormat, OUTPUT_FORMATS


HIDDEN_CMD_LIST = [["auth", "login"], ["auth", "token"], ["config", "set", PROXY_KEY]]


def get_loggable_args(args):
    """
    Return the args list to log, critical data are removed.
    """
    for idx in range(0, len(args)):
        for hidden_sequence in HIDDEN_CMD_LIST:
            sequence_len = len(hidden_sequence)
            if args[idx : idx + sequence_len] == hidden_sequence:
                return args[: idx + sequence_len]
    return args


def show_verbose(ctx, _, value):
    """Eager option, enable logging on stdout"""
    if not value or ctx.resilient_parsing:
        return
    set_verbosity(value)


def set_output_format(ctx, _, value):
    """Eager option, set output format"""
    if not value or ctx.resilient_parsing:
        return
    OutputFormat.from_option = value


def show_version(ctx, _, value):
    """Eager option, show version and exit gmsaas

    To provide several `--version` outputs depending on `--format` option
    we use a custom callback with the help of Click Eager option concept, see
    https://click.palletsprojects.com/en/7.x/options/#callbacks-and-eager-options
    To make it working, `--verbose` and `--format` should be Eager options too.
    Limitation:
    Eager options are evaluated by the order the user provides them to the script.
    As `--version` callback exits gmsaas, `gmsaas --version --format json` would
    output text format, but `gmsaas --format json --verbose --version` works fine.
    """
    if not value or ctx.resilient_parsing:
        return
    ui().show_version(gmsaas.get_name(), gmsaas.get_version(), gmsaas.get_doc_url(), gmsaas.get_pypi_url())
    ctx.exit()


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.option(
    "--verbose",
    "-v",
    count=True,
    is_eager=True,
    callback=show_verbose,
    expose_value=False,
    help="Print logs in stdout.",
)
@click.option(
    "--format",
    type=click.Choice(OUTPUT_FORMATS),
    is_eager=True,
    expose_value=False,
    callback=set_output_format,
    help="Output format to use. You can set a default format with 'gmsaas config set output-format <format>'.",
)
@click.option(
    "--version",
    is_flag=True,
    is_eager=True,
    expose_value=False,
    callback=show_version,
    help="Show the version and exit.",
)
@click.pass_context
def main(ctx):
    """
    Command line client for Genymotion SaaS
    """
    LOGGER.info("==== START args: %s ====", get_loggable_args(sys.argv[1:]))
    setup_proxy()
    ctx.ensure_object(dict)


main.add_command(auth)
main.add_command(config)
main.add_command(instances_cmd_group)
main.add_command(recipes_cmd_group)
main.add_command(osimages_cmd_group)
main.add_command(hwprofiles_cmd_group)
main.add_command(logzip)
main.add_command(doctor)
main.add_command(adb)


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
