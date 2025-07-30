# SPDX-License-Identifier: Apache-2.0

from pathlib import Path
from qa_pytest_rabbitmq.rabbitmq_configuration import RabbitMqConfiguration


class RabbitMqSelfConfiguration(RabbitMqConfiguration):
    def __init__(
            self,
            path: Path = Path("qa-pytest-examples/resources/rabbitmq-self-default-config.ini")):
        super().__init__(path)
