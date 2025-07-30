# SPDX-FileCopyrightText: 2025 Adrian Herscu
#
# SPDX-License-Identifier: Apache-2.0

from dataclasses import asdict
from typing import Iterator, Self, final

from requests import Request
from hamcrest.core.matcher import Matcher
import requests

from qa_pytest_examples.swagger_petstore_configuration import SwaggerPetstoreConfiguration
from qa_pytest_examples.model.swagger_petstore_pet import SwaggerPetstorePet
from qa_pytest_rest.rest_steps import HttpMethod, RestSteps
from qa_testing_utils.logger import traced
from qa_testing_utils.matchers import adapted_object


@final
class SwaggerPetstoreSteps(RestSteps[SwaggerPetstoreConfiguration]):

    def swagger_petstore(self, client: requests.Session):
        self._rest_session = client
        return self

    @traced
    def adding(self, pet: SwaggerPetstorePet) -> Self:
        return self.invoking(Request(
            method=HttpMethod.POST,
            url=self.configured.endpoint_url(path="pet"),
            json=asdict(pet)
        ))

    @traced
    def the_available_pets(self, by_rule: Matcher
                           [Iterator[SwaggerPetstorePet]]) -> Self:
        return self.the_invocation(Request(
            method=HttpMethod.GET,
            url=self.configured.endpoint_url(path="pet/findByStatus"),
            params={"status": "available"}),
            adapted_object(
                lambda response: SwaggerPetstorePet.from_(response),
                by_rule))
