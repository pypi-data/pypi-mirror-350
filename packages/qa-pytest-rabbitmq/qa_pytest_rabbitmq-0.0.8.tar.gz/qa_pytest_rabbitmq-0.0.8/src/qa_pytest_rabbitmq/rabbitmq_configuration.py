# SPDX-License-Identifier: Apache-2.0

import pika
from functools import cached_property
from qa_pytest_commons.base_configuration import BaseConfiguration


class RabbitMqConfiguration(BaseConfiguration):
    @cached_property
    def amqp_url(self) -> pika.URLParameters:
        return pika.URLParameters(self.parser.get("rabbitmq", "amqp_url"))
