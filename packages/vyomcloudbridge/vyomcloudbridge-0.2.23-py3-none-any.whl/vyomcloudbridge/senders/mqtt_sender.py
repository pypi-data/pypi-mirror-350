import time
import threading
import os
import json
import base64
import uuid
from typing import Callable
from awscrt import mqtt
from awsiot import mqtt_connection_builder
from concurrent.futures import TimeoutError
from vyomcloudbridge.utils.configs import Configs
from vyomcloudbridge.utils.logger_setup import setup_logger
from vyomcloudbridge.constants.constants import (
    cert_file_path,
    pri_key_file_path,
    root_ca_file_path,
    MQTT_ENTPOINT,
)
from vyomcloudbridge.utils.abc_sender import AbcSender


class MqttSender(AbcSender):
    def __init__(
        self,
    ):
        try:
            super().__init__()
            self.logger.info("MqttSender initializing...")
            # compulsory
            self.channel = "mqtt"
            self.combine_by_target_id = True

            # machine specific
            self.machine_config = Configs.get_machine_config()
            self.machine_id = self.machine_config.get("machine_id", "-") or "-"
            self.client_id = f"machine{self.machine_id}Prod-{uuid.uuid4().hex[:8]}"

            # class specific
            self.endpoint = MQTT_ENTPOINT
            self.cert_path = cert_file_path
            self.pri_key_path = pri_key_file_path
            self.root_ca_path = root_ca_file_path
            self.client_id = f"machine{self.machine_id}Prod-{uuid.uuid4().hex[:8]}"

            self._verify_cert_files()

            # Connection state tracking
            self.is_connected = False
            self.connection_lock = threading.Lock()
            self._connection_in_progress = False

            # Connection and reconnection parameters
            self.max_reconnect_attempts = 5
            self.base_reconnect_delay = 1  # Base delay in seconds

            # Initialize the MQTT connection
            self.mqtt_connection = None
            self._create_mqtt_connection()

            # Start a connection monitoring thread
            self._start_connection_monitor()
            self.logger.info("MqttSender initialized successfully!")
        except Exception as e:
            self.logger.error(f"Error init MqttSender: {str(e)}")
            raise

    def _verify_cert_files(self):
        for file_path in [self.cert_path, self.pri_key_path, self.root_ca_path]:
            if not os.path.exists(file_path):
                self.logger.error(f"ERROR: File not found: {file_path}")
                raise FileNotFoundError(f"Required file not found: {file_path}")
            else:
                with open(file_path, "r") as f:
                    pass

    def _create_mqtt_connection(self):
        """Create a new MQTT connection with exponential backoff"""
        with self.connection_lock:  # Acquire lock to prevent concurrent attempts
            if self.is_connected:
                self._connection_in_progress = False
                self.logger.info(
                    "Connection already established, skipping reconnection"
                )
                return

            self._connection_in_progress = True
            try:
                for attempt in range(self.max_reconnect_attempts):
                    try:
                        # Use exponential backoff for reconnection attempts
                        delay = self.base_reconnect_delay * (2**attempt)

                        # Create MQTT connection with keep-alive and will message
                        self.mqtt_connection = mqtt_connection_builder.mtls_from_path(
                            endpoint=self.endpoint,
                            cert_filepath=self.cert_path,
                            pri_key_filepath=self.pri_key_path,
                            ca_filepath=self.root_ca_path,
                            client_id=self.client_id,
                            clean_session=False,
                            keep_alive_secs=1200,  # 20 minutes
                            ping_timeout_ms=3000,
                            on_connection_interrupted=self._on_connection_interrupted,
                            on_connection_resumed=self._on_connection_resumed,
                        )

                        # Connect to AWS IoT Core
                        connect_future = self.mqtt_connection.connect()
                        connect_future.result()  # Wait for connection
                        self.is_connected = True
                        self.logger.info("Successfully connected to AWS IoT Core")
                        return

                    except Exception as e:
                        self.logger.error(
                            f"AWS IoT core connection attempt {attempt + 1} failed: {str(e)}"
                        )
                        if attempt < self.max_reconnect_attempts - 1:
                            time.sleep(delay)

                # If all attempts fail
                self.logger.error(
                    "Failed to establish MQTT connection after multiple attempts"
                )
                raise ConnectionError("Could not connect to AWS IoT Core")

            finally:
                self._connection_in_progress = False

    def _on_connection_interrupted(self, connection, error, **kwargs):
        """
        Callback when connection is interrupted
        This method is called automatically by AWS IoT SDK
        """
        self.logger.warning(f"Connection interrupted: {error}")
        with self.connection_lock:
            self.is_connected = False

    def _on_connection_resumed(
        self, connection, return_code, session_present, **kwargs
    ):
        """
        Callback when connection is resumed
        This method is called automatically by AWS IoT SDK
        """
        if return_code == mqtt.ConnectReturnCode.ACCEPTED:
            self.logger.info("Connection resumed successfully")

            with self.connection_lock:
                self.is_connected = True
        else:
            self.logger.error(
                f"Connection resume failed with return code: {return_code}"
            )

    def _start_connection_monitor(self):
        """
        Start a background thread to monitor connection health
        Uses built-in AWS IoT SDK reconnection mechanisms
        """

        def monitor_connection():
            while True:
                try:
                    if not self.is_connected:
                        self.logger.warning(
                            "Connection is down. Attempting to reconnect..."
                        )
                        self._create_mqtt_connection()
                    time.sleep(30)
                except Exception as e:
                    self.logger.error(f"Connection monitoring failed: {str(e)}")

        # Start monitoring in a daemon thread
        monitor_thread = threading.Thread(target=monitor_connection, daemon=True)
        monitor_thread.start()

    def publish_message_to_topic(self, topic: str, payload):
        """
        Publish message with connection state check
        """
        try:
            path_parts = topic.split("/")
            if len(path_parts) > 8:
                self.logger.error(
                    "Topic length exceeded - a maximum of 8 sub-parts are allowed in a topic."
                )
                return False

            is_connection_tried = self._connection_in_progress
            with self.connection_lock:
                if not self.is_connected and is_connection_tried:
                    self.logger.error(
                        f"Publish to {topic} failed: aws iot core is not connected"
                    )
                    return False

            # Outside the lock, create connection if needed
            if not self.is_connected:
                self._create_mqtt_connection()
            self.logger.info(f"Message publishing...... to topic: {topic}")
            publish_future, _ = self.mqtt_connection.publish(
                topic=topic, payload=payload, qos=mqtt.QoS.AT_LEAST_ONCE
            )
            publish_future.result(timeout=10)
            self.logger.info(f"Message published to topic: {topic}")
            return True
        except TimeoutError:
            self.logger.error(f"Publish to {topic} failed: TimeoutError")
            return False
        except Exception as e:
            self.logger.error(
                f"Publish to {topic} failed: {str(e)} , message_type={type(payload)}"
            )
            return False

    def _get_topic(self, dest_id):
        epoch_ms = int(time.time() * 1000)
        filename = f"{epoch_ms}.json"
        return f"vyom-mqtt/message/{dest_id}/{self.machine_id}/{filename}"

    def send_message(
        self,
        message,
        message_type,
        data_source,
        target_des_id,
        destination_id,
        source_id,
        topic,
    ):
        """
        Publish message with connection state check
        """
        try:
            topic = topic if target_des_id == "s3" else self._get_topic(target_des_id)
            return self.publish_message_to_topic(topic, message)
        except Exception as e:
            self.logger.error(
                f"Publish to {topic} failed: {str(e)}, message_type={type(message)}"
            )
            return False

    def is_healthy(self):
        """Gracefully close the MQTT connection"""
        try:
            if self.mqtt_connection:
                disconnect_future = self.mqtt_connection.disconnect()
                disconnect_future.result(timeout=10)
                self.mqtt_connection = None

            with self.connection_lock:
                self.is_connected = False

            self.logger.info("MQTT AWS IoT Core connection closed successfully")

        except Exception as e:
            self.logger.error(f"Failed to close MQTT connection: {str(e)}")

    def cleanup(self):
        """Gracefully close the MQTT connection"""
        try:
            if self.mqtt_connection:
                disconnect_future = self.mqtt_connection.disconnect()
                disconnect_future.result(timeout=10)
                self.mqtt_connection = None

            with self.connection_lock:
                self.is_connected = False

            self.logger.info("MQTT AWS IoT Core connection closed successfully")

        except Exception as e:
            self.logger.error(f"Failed to close MQTT connection: {str(e)}")


logger = setup_logger(name=__name__, show_terminal=True)


def minimal_mqtt_sender_example():
    try:
        # Initialize MqttSender
        sender = MqttSender()
        machine_id = sender.machine_id
        message = {
            "timestamp": "2025-04-10T10:00:00Z",
            "data": {"status": "online", "temperature": 25.5, "humidity": 60},
        }
        result = sender.send_message(
            message=json.dumps(message),
            message_type="json",
            data_source="sample_source",
            target_des_id="s3",
            destination_id="s3",
            source_id=machine_id,
            topic="vyom-mqtt/message/s3/" + str(machine_id) + "/sample_topic",
        )

        if result:
            logger.info("Message sent successfully")
        else:
            logger.error("Failed to send message")

        # Close the connection when done
        sender.cleanup()

    except Exception as e:
        logger.error(f"Error in minimal_mqtt_sender_example: {str(e)}")


if __name__ == "__main__":
    minimal_mqtt_sender_example()
