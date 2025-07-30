# SPDX-License-Identifier: Apache-2.0


from typing import Iterator, Self

from hamcrest.core.matcher import Matcher
from qa_pytest_commons.generic_steps import GenericSteps
from qa_pytest_rabbitmq.queue_handler import Message, QueueHandler
from qa_pytest_rabbitmq.rabbitmq_configuration import RabbitMqConfiguration
from qa_testing_utils.object_utils import require_not_none


class RabbitMqSteps[K, V, TConfiguration: RabbitMqConfiguration](
        GenericSteps[TConfiguration]):
    _queue_handler: QueueHandler[K, V]

    def a_queue_handler(self, queue_handler: QueueHandler[K, V]) -> Self:
        self._queue_handler = queue_handler
        return self

    def publishing(self, messages: Iterator[Message[V]]) -> Self:
        self._queue_handler.publish(messages)
        return self

    def consuming(self) -> Self:
        self._queue_handler.consume()
        return self

    def the_received_messages(
            self, by_rule: Matcher[Iterator[Message[V]]]) -> Self:
        return self.eventually_assert_that(
            lambda: iter(self._queue_handler.received_messages.values()),
            by_rule)

    def the_message_by_key(
            self, key: K, by_rule: Matcher[Message[V]]) -> Self:
        return self.eventually_assert_that(
            lambda: require_not_none(self._queue_handler.received_messages.get(key)),
            by_rule)
