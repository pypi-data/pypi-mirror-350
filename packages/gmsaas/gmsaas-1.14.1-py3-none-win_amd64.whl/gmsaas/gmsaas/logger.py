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
Application logger
"""

import logging
import sys
import time

import gmsaas

from gmsaas.storage.settings import get_gmsaas_log_path

CONSOLE_HANDLER = "logconsole_{}"
FILE_HANDLER = "logfile_{}"


class UTCFormatter(logging.Formatter):
    """Formatter doing the UTC conversion"""

    converter = time.gmtime


def _remove_handler(logger, handler_name):
    handler = next((h for h in logger.handlers if h.name == handler_name), None)
    if handler:
        logger.removeHandler(handler)


def get_logger(verbosity=0, logger_name=gmsaas.__application__, version=gmsaas.__version__):
    """
    Create and configure a logger using a given name.
    """
    application_str = logger_name
    if version:
        application_str += " " + version
    formatter = UTCFormatter(
        fmt=(
            "%(asctime)s.%(msecs)03d "
            "[{application}:%(process)d] "
            "[%(levelname)s] "
            "%(message)s".format(application=application_str)
        ),
        datefmt="%Y-%m-%dT%H:%M:%S",
    )

    local_logger = logging.getLogger(logger_name)

    file_log_name = FILE_HANDLER.format(logger_name)
    _remove_handler(local_logger, file_log_name)
    file_log_handler = logging.FileHandler(get_gmsaas_log_path())
    file_log_handler.set_name(file_log_name)
    file_log_handler.setLevel(logging.DEBUG)
    file_log_handler.setFormatter(formatter)

    local_logger.setLevel(logging.DEBUG)
    local_logger.addHandler(file_log_handler)

    local_logger.verbosity = verbosity

    if verbosity > 0:
        console_log_name = CONSOLE_HANDLER.format(logger_name)
        _remove_handler(local_logger, console_log_name)
        console_log_handler = logging.StreamHandler(sys.stdout)
        console_log_handler.set_name(console_log_name)
        console_log_handler.setLevel(logging.DEBUG)
        console_log_handler.setFormatter(formatter)
        local_logger.addHandler(console_log_handler)

    return local_logger


LOGGER = get_logger(verbosity=0)


def set_verbosity(verbosity):
    """
    Prints logs in stdout
    """
    global LOGGER  # pylint: disable=global-statement
    LOGGER = get_logger(verbosity=verbosity)


def log_elapsed_time(f):
    """Decorator to log the duration of a command."""

    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = f(*args, **kwargs)
        duration = time.time() - start_time
        LOGGER.debug("Operation '%s' executed in %.2f seconds", f.__name__, duration)
        return result

    return wrapper
