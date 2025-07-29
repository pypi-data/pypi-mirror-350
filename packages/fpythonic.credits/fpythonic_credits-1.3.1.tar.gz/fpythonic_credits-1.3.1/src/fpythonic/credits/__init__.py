# Copyright 2023-2025 Geoffrey R. Scheller
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

"""Functional Pythonic Programming  - Namespace package `fpypthonic`

Tools to aid with Python development which tend to take a functional programming
approach yet still endeavoring to remain Pythonic.

"""

from __future__ import annotations

__author__ = 'Geoffrey R. Scheller'
__copyright__ = 'Copyright (c) 2025 Geoffrey R. Scheller'
__license__ = 'Apache License 2.0'

__all__ = [
    'maintainer',
    'copyright',
    'license',
    'display_credits',
]


def maintainer(me: str = __author__) -> str:
    return me


def copyright(copy_right: str = __copyright__) -> str:
    return copy_right


def license(license: str = __license__) -> str:
    return license


def display_credits() -> None:
    msg = 'maintaner: {}\n{}\nlicence: {}'.format(
        maintainer(),
        copyright(),
        license(),
    )
    print(msg)
