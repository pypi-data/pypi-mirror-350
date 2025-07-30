# SPDX-License-Identifier: Apache-2.0

import pika
from typing import Any, Generic, TypeVar, override
from qa_pytest_commons.abstract_tests_base import AbstractTestsBase
from qa_pytest_rabbitmq.rabbitmq_configuration import RabbitMqConfiguration
from qa_pytest_rabbitmq.rabbitmq_steps import RabbitMqSteps


K = TypeVar("K")
V = TypeVar("V")
TConfiguration = TypeVar("TConfiguration", bound=RabbitMqConfiguration)
TSteps = TypeVar("TSteps", bound=RabbitMqSteps[Any, Any, Any])


class RabbitMqTests(
        Generic[K, V, TSteps, TConfiguration],
        AbstractTestsBase[TSteps, TConfiguration]):
    _connection: pika.BlockingConnection

    @override
    def setup_method(self):
        super().setup_method()
        self._connection = pika.BlockingConnection(self._configuration.amqp_url)

    @override
    def teardown_method(self):
        try:
            self._connection.close()
        finally:
            super().teardown_method()
