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
Cli for command logzip
"""

import os
import pathlib

import click

from gmsaas.gmsaas.errors import LogzipError
from gmsaas.saas.logcollector import LogCollector
from gmsaas.cli.clioutput import ui


def validate_zip_path(ctx, _, zip_path: str):
    """
    Check if path is correct:
    - absolute
    - must have read and write permissions
    - if zip_path is a file:
        - parent dir must exist
        - must end with .zip extension
    - if zip_path is a dir:
        - must exist
    """
    del ctx
    if not zip_path:
        return None
    try:
        zip_path = pathlib.Path(os.path.expandvars(zip_path)).expanduser()
        if not zip_path.is_absolute():
            raise click.BadParameter(f"Path `{zip_path}` must be absolute.")
        if zip_path.is_dir():
            if not zip_path.exists():
                raise click.BadParameter(f"Path `{zip_path}` must exist.")
        else:
            if not zip_path.parent.exists():
                raise click.BadParameter(f"Path `{zip_path.parent}` must exist.")
            if not str(zip_path).endswith(".zip"):
                raise click.BadParameter(f"Path `{zip_path}` must end with '.zip'")
    except PermissionError as exception:
        raise click.BadParameter(f"Path `{zip_path.parent}` must have read and write permissions.") from exception
    return str(zip_path)


@click.command("logzip")
@click.option(
    "--out",
    "out_path",
    type=click.Path(),
    callback=validate_zip_path,
    required=False,
    help="Either a ZIP archive path or a directory.",
)
def logzip(out_path):
    """
    Create a ZIP archive containing all 'gmsaas' logs
    """
    collector = LogCollector()
    try:
        archive_path = collector.process(out_path)
    except Exception as exception:
        raise LogzipError(exception) from exception

    ui().logzip(archive_path)
