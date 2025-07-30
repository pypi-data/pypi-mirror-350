import pika
import pika.channel
from pika.spec import Basic
from pika.exceptions import (
    ConnectionClosedByBroker,
    AMQPChannelError,
    AMQPConnectionError,
)
import json
import logging
from typing import Any, Callable
import time
import os
from vyomcloudbridge.utils.logger_setup import setup_logger

logger = setup_logger(name=__name__, show_terminal=False)


class RabbitMQ:
    def __init__(self, host: str = "localhost", queue_name: str = "data_queue"):
        self.host = host
        self.queue_name = queue_name
        self.connection = None
        self.channel = None
        # Don't set up connection in __init__ when running as service
        # It will be set up in consume() instead

    def _setup_connection(self) -> None:
        """Setup connection and channel with retry logic"""
        if self.connection and not self.connection.is_closed:
            try:
                self.connection.close()
            except:
                pass

        max_retries = 5
        for attempt in range(max_retries):
            try:
                self.connection = pika.BlockingConnection(
                    pika.ConnectionParameters(
                        host=self.host,
                        heartbeat=600,
                        blocked_connection_timeout=300,
                        socket_timeout=300,
                    )
                )
                self.channel = self.connection.channel()
                # Declare queue with priority support
                self.channel.queue_declare(
                    queue=self.queue_name,
                    durable=True,
                    arguments={
                        "x-message-ttl": 1000 * 60 * 60 * 24,  # 24 hour TTL
                        "x-max-priority": 10,  # Enable priorities from 0-10
                    },
                )

                # Set QoS
                self.channel.basic_qos(prefetch_count=1)
                logger.info("RabbitMQ connection established")
                return

            except AMQPConnectionError as e:
                if attempt == max_retries - 1:
                    logger.error(
                        f"Failed to connect to RabbitMQ after {max_retries} attempts"
                    )
                    raise
                logger.warning(
                    f"RabbitMQ connection attempt {attempt + 1} failed, retrying..."
                )
                time.sleep(2**attempt)
            except Exception as e:
                if attempt == max_retries - 1:
                    logger.error(
                        f"Failed to connect to RabbitMQ after {max_retries} attempts"
                    )
                    raise
                logger.warning(
                    f"RabbitMQ connection attempt {attempt + 1} failed, retrying..."
                )
                time.sleep(2**attempt)

    def _ensure_connection(self) -> bool:
        """Ensure connection and channel are active and working"""
        try:
            if not self.connection or self.connection.is_closed:
                self._setup_connection()
                return True

            if not self.channel or self.channel.is_closed:
                logger.info("Closed channel found, re-establishing...")
                self.channel = self.connection.channel()
                # Declare queue with priority support
                self.channel.queue_declare(
                    queue=self.queue_name,
                    durable=True,
                    arguments={
                        "x-message-ttl": 1000 * 60 * 60 * 24,  # 24 hour TTL
                        "x-max-priority": 10,  # Enable priorities from 0-10
                    },
                )

                # Set QoS
                self.channel.basic_qos(prefetch_count=1)
                logger.info("Channel re-established successfully")

            return True
        except Exception as e:
            logger.error(f"Failed to ensure connection: {e}")
            self.connection = None
            self.channel = None
            return False

    def publish(self, message: Any, priority: int = 0, expiration: str = None) -> None:
        """Publish message to queue with specified priority (0-10, higher is more priority)"""
        """ expiration is millisecond in string """
        if not self._ensure_connection():
            raise Exception("Could not establish connection")

        # Ensure priority is within bounds
        if priority < 0:
            priority = 0
        elif priority > 10:
            priority = 10
        properties = {
            "delivery_mode": 2,  # Make message persistent
            "content_type": "application/json",
            "priority": priority,  # Always set priority
        }
        if expiration is not None:
            properties["expiration"] = expiration  # 60 seconds TTL

        try:
            self.channel.basic_publish(
                exchange="",
                routing_key=self.queue_name,
                body=json.dumps(message),
                properties=pika.BasicProperties(**properties),
            )
            message_str = (
                json.dumps(message) if not isinstance(message, str) else message
            )
            truncated_message = (
                (message_str[:100] + "...") if len(message_str) > 100 else message_str
            )

            expiry_log = f" with expiration {expiration}ms" if expiration else ""
            logger.info(
                f"Enqueued message to queue {self.queue_name} with priority {priority}{expiry_log}: {truncated_message}"
            )
        except Exception as e:
            logger.error(f"Error publishing message: {e}")
            self._setup_connection()
            self.publish(message, priority, expiration)

    def _process_message(
        self,
        callback: Callable,
        channel: pika.channel.Channel,
        method_frame: Basic.Deliver,
        properties: pika.BasicProperties,
        body,
    ):
        """Process a single message"""
        try:
            message = json.loads(body)
            queue_name = method_frame.routing_key
            priority = properties.priority if properties.priority is not None else 0
            new_priority = max(priority - 1, 0) if priority < 3 else priority  # TODO

            expiry_info = ""
            if hasattr(properties, "expiration") and properties.expiration:
                expiry_info = f" with expiration {properties.expiration}ms"
            logger.info(
                f"Processing message from {queue_name} with priority {priority}{expiry_info}"
            )
            result = callback(message)

            if result:
                channel.basic_ack(delivery_tag=method_frame.delivery_tag)
                logger.info(f"Message processed successfully in {queue_name}")
            else:
                # If processing failed, republish with mew priority instead of just nacking
                logger.warning(
                    f"Message processing failed in {queue_name}, requeuing with new priority {new_priority}"
                )
                # First ack the original message
                channel.basic_ack(delivery_tag=method_frame.delivery_tag)

                new_properties = {
                    "priority": new_priority,
                    "content_type": properties.content_type,
                    "delivery_mode": properties.delivery_mode,  # Preserve persistence setting
                }

                if hasattr(properties, "expiration") and properties.expiration:
                    new_properties["expiration"] = properties.expiration

                if hasattr(properties, "headers") and properties.headers:
                    new_properties["headers"] = properties.headers

                if (
                    hasattr(properties, "content_encoding")
                    and properties.content_encoding
                ):
                    new_properties["content_encoding"] = properties.content_encoding

                channel.basic_publish(
                    exchange="",  # Use default exchange
                    routing_key=queue_name,
                    body=body,
                    properties=pika.BasicProperties(**new_properties),
                )

        except Exception as e:
            logger.error(f"Error processing message in {queue_name}: {e}")

            # For exceptions, also republish with new priority
            try:
                priority = properties.priority if properties.priority is not None else 0
                logger.warning(
                    f"Error processing message, requeuing with new priority {new_priority}"
                )
                # First ack the original message
                channel.basic_ack(delivery_tag=method_frame.delivery_tag)

                new_properties = {
                    "priority": new_priority,
                    "content_type": properties.content_type,
                    "delivery_mode": properties.delivery_mode,  # Preserve persistence setting
                }

                if hasattr(properties, "expiration") and properties.expiration:
                    new_properties["expiration"] = properties.expiration

                if hasattr(properties, "headers") and properties.headers:
                    new_properties["headers"] = properties.headers

                if (
                    hasattr(properties, "content_encoding")
                    and properties.content_encoding
                ):
                    new_properties["content_encoding"] = properties.content_encoding

                channel.basic_publish(
                    exchange="",
                    routing_key=queue_name,
                    body=body,
                    properties=pika.BasicProperties(**new_properties),
                )
            except Exception as republish_error:
                logger.error(
                    f"Failed to republish message with new priority: {republish_error}"
                )
                channel.basic_nack(delivery_tag=method_frame.delivery_tag, requeue=True)

    def consume(self, callback: Callable) -> None:
        """Start consuming messages with priority handling by RabbitMQ"""
        # Establish initial connection
        if not self._ensure_connection():
            raise Exception("Could not establish initial connection")

        logger.info(f"Started consuming messages from {self.queue_name}...")

        while True:
            try:
                if not self._ensure_connection():
                    logger.warning("Connection lost, waiting before retry...")
                    time.sleep(1)
                    continue

                # Setup consumer with the callback
                def callback_wrapper(channel, method, properties, body):
                    self._process_message(callback, channel, method, properties, body)

                self.channel.basic_consume(
                    queue=self.queue_name,
                    on_message_callback=callback_wrapper,
                    auto_ack=False,  # We'll handle acknowledgments manually
                )

                # Start consuming - this will block until channel or connection is closed
                self.channel.start_consuming()

            except ConnectionClosedByBroker:
                logger.warning("Connection closed by broker, reconnecting...")
                time.sleep(1)
            except AMQPChannelError as e:
                logger.error(f"Channel error: {e}")
                time.sleep(1)
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                time.sleep(1)
                self._setup_connection()

    def close(self) -> None:
        """Close connection"""
        if self.connection and not self.connection.is_closed:
            try:
                logger.info("Service RabbitMQ shutdown signal, connection closing...")
                self.connection.close()
                logger.info("Connection closed")
            except Exception as e:
                logger.error(f"Error closing connection: {e}")
        else:
            logger.info("RabbitMQ already cleaned, no active connection")

    def is_healthy(self):
        """
        Check if the service is healthy.
        """
        return (
            hasattr(self, "connection") and self.connection and self.connection.is_open
        )

    def __del__(self):
        """Destructor called by garbage collector to ensure resources are cleaned up, when object is about to be destroyed"""
        try:
            logger.error("Destructor called by garbage collector to cleanup RabbitMQ")
            self.close()
        except Exception as e:
            pass
