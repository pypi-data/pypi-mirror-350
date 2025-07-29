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
Module related to dict data
"""


def safe_get(iter_obj, keys, default_value):
    """
    Retrieve any value of a dict according to `keys`.
    Params:
        iter_obj: dict to search in
        keys: either str (first level) or list of str (for deep search)
        default_value: value returned if keys is not present
    Return:
        Value corresponding to keys if found, default_value otherwise
    Example:
        Given:

        iter_obj = {
            "a": {
                "b": {
                    "c": [
                        {"d": 666}
                    ]
                }
            },
            "aa": 42
        }

        with keys = "aa", return is 42
        with keys = ["a", "b", "c", "e"], return is default_value
        with keys = ["a", "b", "c", 0, "d"], return is 666
    """
    if isinstance(keys, str):
        keys = [keys]
    for key in keys:
        try:
            iter_obj = iter_obj[key]
        except TypeError:
            return default_value
        except KeyError:
            return default_value
        except IndexError:
            return default_value
    return iter_obj
