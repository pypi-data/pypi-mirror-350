#!/usr/bin/env python3
"""
MachineStats Service

This script monitors RabbitMQ queue sizes and reports the buffer size to an API endpoint.
It runs as a standalone service and continues monitoring regardless of other services.

"""

from datetime import datetime, timezone
import time
import os
import requests
import threading
import signal
import sys
import json
import pika
import argparse
from typing import Dict, Any, Optional
from vyomcloudbridge.services.rabbit_queue.queue_main import RabbitMQ
from vyomcloudbridge.utils.common import ServiceAbstract
from vyomcloudbridge.utils.configs import Configs
from vyomcloudbridge.constants.constants import BUFFER_API_URL
from vyomcloudbridge.utils.logger_setup import setup_logger
from vyomcloudbridge.utils.common import get_mission_upload_dir
from vyomcloudbridge.constants.constants import default_project_id, default_mission_id, data_buffer_key

# Configuration
RABBITMQ_HOST = "localhost"
RABBITMQ_QUEUE_PREFIX = "data_queue"
REPORTING_INTERVAL = 5  # seconds
AVG_MESSAGE_SIZE = 500 * 1024  # 500 KB average message size in bytes
HEADERS = {"Content-Type": "application/json"}


class RabbitMQMonitor:
    """Monitor RabbitMQ queues and report buffer size."""

    def __init__(self, host: str, queue_prefix: str):
        """
        Initialize the RabbitMQ monitor.

        Args:
            host: RabbitMQ host address
            queue_prefix: Prefix for queue names
        """
        self.host = host
        self.queue_p1 = f"{queue_prefix}_p1"
        self.queue_p2 = f"{queue_prefix}_p2"
        self.connection = None
        self.channel = None
        self.logger = setup_logger(
            name=self.__class__.__module__ + "." + self.__class__.__name__,
            show_terminal=False,
        )

    def _setup_connection(self) -> None:
        """Setup connection and channel with retry logic."""
        if self.connection and not self.connection.is_closed:
            try:
                self.connection.close()
            except Exception:
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

                # Declare both queues
                for queue_name in [self.queue_p1, self.queue_p2]:
                    self.channel.queue_declare(
                        queue=queue_name,
                        durable=True,
                        arguments={"x-message-ttl": 1000 * 60 * 60 * 24},  # 24 hour TTL
                    )

                self.logger.info("RabbitMQMonitor connection established")
                return

            except pika.exceptions.AMQPConnectionError as e:
                if attempt == max_retries - 1:
                    self.logger.error(
                        f"Failed to connect to RabbitMQ after {max_retries} attempts: {e}"
                    )
                    raise
                self.logger.warning(
                    f"RabbitMQMonitor connection attempt {attempt + 1} failed, retrying..."
                )
                time.sleep(2**attempt)

    def ensure_connection(self) -> bool:
        """
        Ensure connection is active and working.

        Returns:
            True if connection is established, False otherwise
        """
        try:
            if not self.connection or self.connection.is_closed:
                self._setup_connection()
            return True
        except Exception as e:
            self.logger.error(f"Failed to ensure connection: {e}")
            return False

    def get_queue_sizes(self) -> tuple:
        """
        Get sizes of both priority queues.

        Returns:
            Tuple of (p1_count, p2_count, total_size_bytes)
        """
        if not self.ensure_connection():
            return 0, 0, 0

        try:
            # Get message counts for each queue
            p1_count = 0
            p2_count = 0

            try:
                p1_info = self.channel.queue_declare(queue=self.queue_p1, passive=True)
                p1_count = p1_info.method.message_count
            except Exception as e:
                self.logger.error(f"Error getting P1 queue info: {e}")

            try:
                p2_info = self.channel.queue_declare(queue=self.queue_p2, passive=True)
                p2_count = p2_info.method.message_count
            except Exception as e:
                self.logger.error(f"Error getting P2 queue info: {e}")

            # Calculate total size
            total_count = p1_count + p2_count
            total_size_bytes = total_count * AVG_MESSAGE_SIZE

            return p1_count, p2_count, total_size_bytes

        except Exception as e:
            self.logger.error(f"Error getting queue sizes: {e}")
            return 0, 0, 0

    def close(self):
        """Close the RabbitMQ connection."""
        if self.connection and not self.connection.is_closed:
            try:
                self.connection.close()
                self.logger.info("RabbitMQ connection closed")
            except Exception as e:
                self.logger.error(f"Error closing RabbitMQ connection: {e}")

    def is_healthy(self):
        """
        Check if the service is healthy.

        Returns:
            bool: True if the service is running and RabbitMQ connection is healthy
        """
        return (
            hasattr(self, "connection") and self.connection and self.connection.is_open
        )

    def __del__(self):
        """Destructor called by garbage collector to ensure resources are cleaned up, when object is about to be destroyed"""
        try:
            self.logger.error(
                "Destructor called by garbage collector to cleanup RabbitMQMonitor"
            )
            self.stop()
        except Exception as e:
            pass


class MachineStats(ServiceAbstract):
    """
    Monitor RabbitMQ queues and report buffer size to API endpoint.
    """

    def __init__(self):
        super().__init__()
        self.machine_config = Configs.get_machine_config()
        self.machine_id = self.machine_config.get("machine_id", "-") or "-"
        self.organization_id = self.machine_config.get("organization_id", "-") or "-"
        self.rabbit_mq_monitor = RabbitMQMonitor(
            host=RABBITMQ_HOST, queue_prefix=RABBITMQ_QUEUE_PREFIX
        )
        self.is_running = False
        self.monitor_thread = None
        self.stop_event = threading.Event()
        self.last_successful_report_time = 0
        self.consecutive_failures = 0
        self.rabbit_mq = RabbitMQ()
        self.data_source = "machine_stats"
        self.logger.info(f"MachineStats initialized for machine ID: {self.machine_id}")

    def _setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown."""

        def signal_handler(sig, frame):
            self.logger.info(f"Received signal {sig}, shutting down MachineStats...")
            self.stop()
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

    def report_buffer_size(self) -> bool:
        """
        Send buffer size to API endpoint with retry logic.

        Returns:
            True if report was successful, False otherwise
        """
        # Get queue sizes
        p1_count, p2_count, buffer_size_bytes = self.rabbit_mq_monitor.get_queue_sizes()

        # Prepare payload
        payload = {
            "machine_id": self.machine_id,
            "buffer": f"{buffer_size_bytes:.2f}",
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
        # Log current state
        self.logger.debug(
            f"Current buffer state: P1: {p1_count} msgs, P2: {p2_count} msgs, Total: {buffer_size_bytes:.2f} bytes"
        )

        try:
            now = datetime.now(timezone.utc)
            date = now.strftime("%Y-%m-%d")
            filename = int(time.time() * 1000)
            # mission_upload_dir = f"{self.machine_config['organization_id']}/{default_project_id}/{date}/{self.data_source}/{self.machine_id}" # TODO
            mission_upload_dir: str = get_mission_upload_dir(
                organization_id=self.organization_id,
                machine_id=self.machine_id,
                mission_id=default_mission_id,
                data_source=self.data_source,
                date=date,
                project_id=default_project_id,
            )
            fileinfo_message = {
                "data": json.dumps(payload),
                "topic": f"{mission_upload_dir}/{filename}.json",
                "message_type": "json",
                "destination_ids": ["s3"],
                "data_source": self.data_source,
                # meta data
                "buffer_key": data_buffer_key,
                "buffer_size": 0,
            }
            self.rabbit_mq.publish(fileinfo_message, 1)
            self.logger.info(f"Machine stats publish SUCCESSFUL")
            return True

            # response = requests.post(
            #     BUFFER_API_URL,
            #     json=payload,
            #     headers=HEADERS,
            #     timeout=5,  # Shorter timeout for frequent calls
            # )

            # if response.status_code == 200:
            #     if attempt > 1:
            #         self.logger.info(
            #             f"Successfully reported buffer size after {attempt} attempts"
            #         )
            #     else:
            #         self.logger.info(
            #             f"Buffer size reported: {buffer_size_bytes:.2f} bytes, (P1: {p1_count}, P2: {p2_count})"
            #         )

            #     self.consecutive_failures = 0
            #     self.last_successful_report_time = time.time()
            #     return True
            # else:
            #     self.logger.warning(
            #         f"API request failed"
            #         f"Status code {response.status_code}, Response: {response.text}"
            #     )
        except requests.exceptions.Timeout:
            self.logger.error(f"Machine stats publish timed out Error")
        except requests.exceptions.ConnectionError:
            self.logger.error(f"Machine stats publish Connection Error")
        except Exception as e:
            self.logger.error(f"Machine stats publish: Unexpected error: {e}")
        return False

    def monitor_loop(self):
        """Main monitoring loop. Runs until stop_event is set."""
        self.logger.info("MachineStats started")

        while not self.stop_event.is_set() and self.is_running:
            try:
                self.report_buffer_size()
            except Exception as e:
                self.logger.error(f"Unexpected error in monitor loop: {e}")
                import traceback

                self.logger.error(f"Traceback: {traceback.format_exc()}")

            # Wait for next reporting interval
            self.stop_event.wait(REPORTING_INTERVAL)

        self.logger.info("MachineStats stopped")

    def start(self):
        """Start the monitoring thread."""
        self.logger.info("Starting MachineStats service")

        try:
            if self.is_running:
                self.logger.warning("MachineStats service is already running")
                return

            # Initialize RabbitMQ connection if needed
            if not self.rabbit_mq_monitor.ensure_connection():
                self.logger.error(
                    "Failed to establish RabbitMQ connection, service not started"
                )
                return

            self.is_running = True
            self.stop_event.clear()

            # Create and start the monitor thread
            self.monitor_thread = threading.Thread(
                target=self.monitor_loop, daemon=True, name="BufferMonitorThread"
            )
            self.monitor_thread.start()

            self.logger.info("MachineStats service started successfully")

        except Exception as e:
            self.is_running = False
            self.logger.error(f"Error starting MachineStats service: {e}")
            import traceback

            self.logger.error(f"Traceback: {traceback.format_exc()}")
            raise

    def stop(self):
        """Stop the monitoring thread."""
        self.logger.info("Stopping MachineStats service...")

        if not self.is_running:
            self.logger.warning("MachineStats service is not running")
            return

        self.is_running = False
        self.stop_event.set()

        if self.monitor_thread and self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=5)
            if self.monitor_thread.is_alive():
                self.logger.warning("Monitor thread did not terminate gracefully")

        # Clean up RabbitMQ connection
        try:
            if self.rabbit_mq_monitor:
                self.rabbit_mq_monitor.close()
                self.logger.info("RabbitMQ connection closed")
        except Exception as e:
            self.logger.error(f"Error closing RabbitMQ connection: {e}")

        self.logger.info("MachineStats service stopped")

    def is_healthy(self):
        """
        Check if the service is healthy.

        Returns:
            bool: True if the service is running and RabbitMQ connection is healthy
        """
        return (
            self.is_running
            and self.rabbit_mq.is_healthy()
            and self.rabbit_mq_monitor.is_healthy()
        )

    def __del__(self):
        """Destructor called by garbage collector to ensure resources are cleaned up, when object is about to be destroyed"""
        try:
            self.logger.error(
                "Destructor called by garbage collector to cleanup MachineStats"
            )
            self.stop()
        except Exception as e:
            pass


def main():
    """Main entry point for the MachineStats service."""
    try:
        print("Starting MachineStats service")

        # Create and start the MachineStats
        buffer_monitor = MachineStats()
        buffer_monitor.start()

        # Keep the main thread alive
        while buffer_monitor.is_running:
            try:
                time.sleep(10)
            except KeyboardInterrupt:
                print("MachineStats service interrupted by user")
                break

    except Exception as e:
        print(f"Fatal error in MachineStats service: {e}")
        import traceback

        print(f"Traceback: {traceback.format_exc()}")

        # Wait and restart on critical error
        time.sleep(5)
        print("Attempting to restart MachineStats service...")
        main()
    finally:
        # if "buffer_monitor" in locals():
        print("Stopping MachineStats service")
        buffer_monitor.stop()


if __name__ == "__main__":
    main()
