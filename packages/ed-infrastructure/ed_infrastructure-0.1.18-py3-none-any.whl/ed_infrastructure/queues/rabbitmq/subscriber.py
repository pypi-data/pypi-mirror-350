import time
from typing import Generic, List, TypeVar

import jsons
from ed_domain.common.logging import get_logger
from ed_domain.queues.common.abc_subscriber import (ABCSubscriber,
                                                    CallbackFunction)
from pika import ConnectionParameters, URLParameters, spec
from pika.adapters import BlockingConnection
from pika.adapters.blocking_connection import BlockingChannel

LOG = get_logger()
TMessageSchema = TypeVar("TMessageSchema")


class RabbitMQSubscriber(Generic[TMessageSchema], ABCSubscriber[TMessageSchema]):
    def __init__(
        self,
        url: str,
        queue: str,
    ) -> None:
        self._queue = queue
        self._connection = self._connect_with_url_parameters(url)
        self._callback_functions: List[CallbackFunction] = []

    def add_callback_function(self, callback_function: CallbackFunction) -> None:
        self._callback_functions.append(callback_function)

    def start(self) -> None:
        LOG.info("Starting subscriber...")
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue=self._queue, durable=True)

        self._channel.basic_consume(
            queue=self._queue, on_message_callback=self._callback, auto_ack=False
        )
        try:
            self._channel.start_consuming()
        except Exception as e:
            LOG.error(f"Error while consuming messages: {e}")
            self.stop()

    def stop(self) -> None:
        LOG.info("Stopping subscriber")
        if self._connection.is_open:
            self._connection.close()

    def _connect_with_connection_parameters(
        self, host: str, port: int
    ) -> BlockingConnection:
        connection_parameters = ConnectionParameters(host, port)
        return BlockingConnection(connection_parameters)

    def _connect_with_url_parameters(self, url: str) -> BlockingConnection:
        connection_parameters = URLParameters(url)
        retry_attempts = 5
        for attempt in range(retry_attempts):
            try:
                return BlockingConnection(connection_parameters)
            except Exception as e:
                LOG.error(f"Connection attempt {attempt + 1} failed: {e}")
                time.sleep(2**attempt)

        raise ConnectionError(
            "Failed to connect to RabbitMQ after several attempts")

    def _callback(
        self,
        channel: BlockingChannel,
        method: spec.Basic.Deliver,
        properties: spec.BasicProperties,
        body: bytes,
    ) -> None:
        """
        Callback function to process received messages.
        """
        try:
            message: TMessageSchema = jsons.loads(body.decode("utf-8"))

            for fn in self._callback_functions:
                fn(message)

            channel.basic_ack(delivery_tag=method.delivery_tag)

        except jsons.DeserializationError as e:
            LOG.error(f"Failed to deserialize message: {e}")
            channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

        except KeyError as e:
            LOG.error(f"Missing key in message: {e}")
            channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

        except Exception as e:
            LOG.error(f"Unexpected error: {e}")
            channel.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
