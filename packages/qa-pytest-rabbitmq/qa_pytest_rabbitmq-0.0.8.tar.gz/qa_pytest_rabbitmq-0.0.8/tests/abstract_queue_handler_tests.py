# SPDX-License-Identifier: Apache-2.0
"""
Abstract base for QueueHandler tests, ported from Java AbstractQueueHandlerTest.
"""
from abc import ABC
from functools import cached_property
import logging
import pika
from tenacity import Retrying, before_sleep_log, retry_if_exception_type, stop_after_attempt, wait_exponential
from qa_testing_utils.logger import LoggerMixin


class AbstractQueueHandlerTests(ABC, LoggerMixin):
    @cached_property
    def local_rabbit_mq(self) -> pika.URLParameters:
        return pika.URLParameters("amqp://guest:guest@localhost")

    @cached_property
    def retrying(self) -> Retrying:
        return Retrying(
            stop=stop_after_attempt(4),
            wait=wait_exponential(min=1, max=10),
            retry=retry_if_exception_type(Exception),
            before_sleep=before_sleep_log(self.log, logging.DEBUG)
        )
