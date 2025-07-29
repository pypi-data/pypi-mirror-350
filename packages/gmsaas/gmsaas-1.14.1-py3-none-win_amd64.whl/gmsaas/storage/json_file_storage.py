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
File Storage using JSON format
"""

import os
import json
import tempfile
from contextlib import contextmanager

from gmsaas.storage.storage import BaseStorage
from gmsaas.storage.settings import get_tmp_path


@contextmanager
def atomic_write(filename):
    """Return a writeable file object that atomically updates a file (using a temporary file)."""
    try:
        tmp_file = tempfile.NamedTemporaryFile(dir=get_tmp_path(), mode="w", encoding="utf-8", delete=False)
        yield tmp_file
        tmp_file.flush()
        os.fsync(tmp_file.fileno())
        tmp_file.close()
        os.replace(tmp_file.name, filename)
    finally:
        try:
            os.remove(tmp_file.name)
        except FileNotFoundError:
            pass


class JsonFileStorage(BaseStorage):
    """Storage implementation that keeps object in a json file"""

    def __init__(self, filename, target_version, permission_flags=None):
        self.filename = filename
        self.permission_flags = permission_flags
        BaseStorage.__init__(self, target_version)

    def _load(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as json_file:
                return json.load(json_file)
        except Exception:
            return {}

    def _save(self, data):
        # Here we ensure the file never gets corrupted at writing time.
        # This happens when much gmsaas instances are working in parallel.
        # It fixes the following scenario:
        # - Set GMSAAS_FORCE_JWT_REFRESH=1 to stress the JWT saving.
        # - Run `run_gmsaas_bench --count=N` with N>=10.
        with atomic_write(self.filename) as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=True)

        if self.permission_flags:
            os.chmod(self.filename, self.permission_flags)
