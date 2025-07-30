# SPDX-FileCopyrightText: 2025 Adrian Herscu
#
# SPDX-License-Identifier: Apache-2.0

from dataclasses import dataclass


@dataclass
class Credentials:
    username: str
    password: str

    @classmethod
    def from_(cls, colon_separated: str):
        return cls(*colon_separated.split(":"))
