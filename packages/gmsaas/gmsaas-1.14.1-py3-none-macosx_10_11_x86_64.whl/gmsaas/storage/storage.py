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
""" Base implementation for storage """
from abc import ABC, abstractmethod


VERSION_KEY = "version"


class BaseStorage(ABC):
    """Abstract class to implement storage of object"""

    def __init__(self, target_version):
        self._target_version = target_version
        self._store = self._load()

    def get(self, key):
        """Get a value for key from storage or None"""
        return self._store.get(key)

    def get_version(self):
        """Get the actual version of the storage"""
        return self.get(VERSION_KEY)

    def put(self, key, value):
        """Save a value for key to storage"""
        self._store[key] = value
        self._store[VERSION_KEY] = self._target_version
        self._save(self._store)

    def remove(self, key):
        """Remove a key/value from storage"""
        self._store.pop(key, None)
        self._save(self._store)

    def get_all(self):
        """Get all key/value from storage (without version key)"""
        data = self._store.copy()
        data.pop(VERSION_KEY, None)
        return data

    def clear(self):
        """Clear all storage"""
        self._store = {}
        self._save(self._store)

    @abstractmethod
    def _load(self):
        """Return dict of loaded content"""

    @abstractmethod
    def _save(self, data):
        """Save data dict"""
