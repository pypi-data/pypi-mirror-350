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
gmsaas crypto functions
"""
import base64


PARTS = [";3@uýP`i", "Ì«w¨H%Á0", "@%¥mV6¸7", "%H²y6¨JB"]


def _get_xor_key():
    result = ""
    for i, current in enumerate(PARTS):
        result += _cypher_v2(PARTS[i - 1], current)
    return result


def cypher_v1(value):
    """
    Cypher a value (string)
    """
    if value is None:
        return None
    if not value:
        return ""

    return base64.b64encode(value.encode("utf-8")).decode("utf-8")


def decypher_v1(cyphered_value):
    """
    Decypher a value (string)
    """
    if cyphered_value is None:
        return None
    if not cyphered_value:
        return ""

    return base64.b64decode(cyphered_value.encode("utf-8")).decode("utf-8")


def _cypher_v2(key, value):
    if value is None:
        return None
    if not value:
        return ""

    key_len = len(key)
    xored_value = ""

    for i, current in enumerate(value):
        current_key = key[i % key_len]
        xored_value += chr(ord(current) ^ ord(current_key))
    return xored_value


def cypher_v2(value):
    """
    XORirify a value (string)
    """
    return _cypher_v2(_get_xor_key(), value)


def decypher_v2(value):
    """
    Convenient function which calls cypher_v2
    """
    return cypher_v2(value)
