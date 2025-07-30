# SPDX-FileCopyrightText: 2025 Adrian Herscu
#
# SPDX-License-Identifier: Apache-2.0

from pathlib import Path
from qa_pytest_rest.rest_configuration import RestConfiguration


class SwaggerPetstoreConfiguration(RestConfiguration):

    def __init__(
            self,
            path: Path = Path("qa-pytest-examples/resources/swagger-petstore-default-config.ini")):
        super().__init__(path)
