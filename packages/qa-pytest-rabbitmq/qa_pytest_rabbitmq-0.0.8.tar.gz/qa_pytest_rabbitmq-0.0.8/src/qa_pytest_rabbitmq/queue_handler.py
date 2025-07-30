# SPDX-License-Identifier: Apache-2.0

import threading
import queue
from typing import Any, Callable, Iterator, Mapping, TypeVar, Generic
from dataclasses import dataclass, field
from types import TracebackType
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import BasicProperties

from qa_testing_utils.logger import LoggerMixin
from qa_testing_utils.object_utils import require_not_none
from qa_testing_utils.string_utils import EMPTY_STRING, to_string

V = TypeVar("V")
K = TypeVar("K")


@to_string()
@dataclass(frozen=True)
class Message(Generic[V]):
    content: V
    properties: BasicProperties = field(default_factory=BasicProperties)


@to_string()
@dataclass
class QueueHandler(Generic[K, V], LoggerMixin):
    channel: BlockingChannel
    queue_name: str
    indexing_by: Callable[[Message[V]], K]
    consuming_by: Callable[[bytes], V]
    publishing_by: Callable[[V], bytes]

    _received_messages: dict[K, Message[V]] = field(
        default_factory=lambda: dict())
    _command_queue: queue.Queue[Callable[[], None]] = field(
        default_factory=lambda: queue.Queue())
    _worker_thread: threading.Thread = field(init=False)
    _shutdown_event: threading.Event = field(
        default_factory=threading.Event, init=False)
    _consumer_tag: str | None = field(default=None, init=False)
    _lock: threading.RLock = field(default_factory=threading.RLock, init=False)

    def __post_init__(self) -> None:
        self._worker_thread = threading.Thread(
            target=self._worker_loop, name="rabbitmq-handler", daemon=True
        )
        self._worker_thread.start()

    def __enter__(self) -> "QueueHandler[K, V]":
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None
    ) -> None:
        self.close()

    def _worker_loop(self) -> None:
        while not self._shutdown_event.is_set():
            try:
                self.channel.connection.process_data_events()
                try:
                    command = self._command_queue.get_nowait()
                    command()
                except queue.Empty:
                    pass
            except Exception as e:
                self.log.error(f"Unhandled error in worker thread: {e}")

    def _submit(self, fn: Callable[[], None]) -> None:
        self._command_queue.put(fn)

    def consume(self) -> str:
        def _consume():
            def on_message(ch: BlockingChannel, method: Any,
                           props: BasicProperties, body: bytes) -> None:
                try:
                    content = self.consuming_by(body)
                    message = Message(content=content, properties=props)
                    key = self.indexing_by(message)
                    with self._lock:
                        self._received_messages[key] = message
                    ch.basic_ack(
                        delivery_tag=require_not_none(
                            method.delivery_tag))
                    self.log.debug(f"received {key}")
                except Exception as e:
                    self.log.warning(f"skipping message due to error: {e}")
                    ch.basic_reject(
                        delivery_tag=require_not_none(
                            method.delivery_tag),
                        requeue=True)

            self._consumer_tag = self.channel.basic_consume(
                queue=self.queue_name, on_message_callback=on_message
            )
            self.log.debug(f"consumer set up with tag {self._consumer_tag}")

        self._submit(_consume)
        return "pending-tag"

    def cancel(self) -> str:
        def _cancel():
            if self._consumer_tag:
                self.channel.connection.add_callback_threadsafe(
                    self.channel.stop_consuming)
                self._consumer_tag = None
                self.log.debug("consumer cancelled")
        self._submit(_cancel)
        return self._consumer_tag or ""

    def publish(self, messages: Iterator[Message[V]]) -> None:
        def _publish():
            for message in messages:
                body = self.publishing_by(message.content)
                self.channel.basic_publish(
                    exchange=EMPTY_STRING,
                    routing_key=self.queue_name,
                    body=body,
                    properties=message.properties
                )
                self.log.debug(f"published {message}")
        self._submit(_publish)

    def publish_values(self, values: Iterator[V]) -> None:
        self.publish((Message(content=value) for value in values))

    def close(self) -> None:
        self.cancel()
        self._shutdown_event.set()
        self._worker_thread.join(timeout=5.0)

    @property
    def received_messages(self) -> Mapping[K, Message[V]]:
        with self._lock:
            return dict(self._received_messages)
