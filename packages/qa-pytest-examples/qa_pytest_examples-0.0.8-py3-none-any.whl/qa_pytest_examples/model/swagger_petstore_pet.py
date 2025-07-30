# SPDX-FileCopyrightText: 2025 Adrian Herscu
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations
from dataclasses import dataclass
from typing import Iterator
from uuid import uuid4

from requests import Response

from qa_testing_utils.string_utils import to_string


@dataclass(eq=True, frozen=True)
@to_string()
class SwaggerPetstorePet:
    name: str
    status: str

    @staticmethod
    def random() -> SwaggerPetstorePet:
        return SwaggerPetstorePet(name=str(uuid4()), status="available")

    @staticmethod
    def from_(response: Response) -> Iterator[SwaggerPetstorePet]:
        return (
            SwaggerPetstorePet(name=pet["name"], status=pet["status"])
            for pet in response.json()
            if "name" in pet and "status" in pet
        )
