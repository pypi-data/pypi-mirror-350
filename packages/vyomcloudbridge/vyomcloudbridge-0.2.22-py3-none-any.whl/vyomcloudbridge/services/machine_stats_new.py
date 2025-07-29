import pika
import json
import logging
from datetime import datetime, timezone
import threading
import time
from typing import Dict, Any, Optional
from vyomcloudbridge.services.rabbit_queue.queue_main import RabbitMQ
from vyomcloudbridge.utils.common import ServiceAbstract, get_mission_upload_dir
from vyomcloudbridge.constants.constants import (
    DEFAULT_RABBITMQ_URL,
    default_project_id,
    default_mission_id,
    data_buffer_key,
)
from vyomcloudbridge.utils.configs import Configs


class MachineStats(ServiceAbstract):
    """
    A service that maintains machine buffer statistics using RabbitMQ as a persistent store.
    Stores the current buffer state in a dedicated queue and publishes stats to HQ.
    """

    def __init__(self):
        """
        Initialize the machine stats service with RabbitMQ connection.
        """
        super().__init__()
        self.host: str = "localhost"
        self.rabbitmq_url = DEFAULT_RABBITMQ_URL
        self.stats_publish_interval = 30  # Seconds between stats publication
        self.publish_error_delay = 60  # Delay after publish error
        
        self.connection = None
        self.channel = None
        self.rabbit_mq = RabbitMQ()
        self.machine_config = Configs.get_machine_config()
        self.machine_id = self.machine_config.get("machine_id", "-") or "-"
        self.organization_id = self.machine_config.get("organization_id", "-") or "-"
        self.data_source = "machine_stats"
        
        # Thread attributes
        self.stats_thread = None
        self.is_running = False
        
        self._setup_connection()

    def _setup_connection(self):
        """Set up RabbitMQ connection and declare the queue for machine buffer."""
        try:
            # Establish connection
            self.connection = pika.BlockingConnection(
                pika.URLParameters(self.rabbitmq_url)
            )
            self.channel = self.connection.channel()
            
            # Declare queue for machine buffer
            self.channel.queue_declare(queue="machine_buffer", durable=True)
            
            self.logger.info("RabbitMQ connection established successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize RabbitMQ: {str(e)}")
            raise

    def _ensure_connection(self) -> bool:
        """Ensure connection is active and working"""
        try:
            if not self.connection or self.connection.is_closed:
                self._setup_connection()
            return True
        except Exception as e:
            self.logger.error(f"Failed to ensure connection: {e}")
            return False

    def get_current_buffer(self) -> int:
        """
        Get the current buffer size from RabbitMQ.

        Returns:
            Current buffer size in bytes or 0 if not found
        """
        try:
            if not self._ensure_connection():
                raise Exception("Could not establish connection")

            method_frame, _, body = self.channel.basic_get(
                queue="machine_buffer", auto_ack=False
            )

            buffer_size = 0
            if method_frame:
                buffer_size = int(body.decode("utf-8"))
                self.channel.basic_nack(
                    delivery_tag=method_frame.delivery_tag, requeue=True
                )
                self.logger.debug(f"Retrieved current buffer size: {buffer_size} bytes")
            return buffer_size
        except Exception as e:
            self.logger.warning(f"Warning getting current buffer: {str(e)}")
            return 0

    def set_current_buffer(self, size: int):
        """
        Update the current buffer size in RabbitMQ.

        Args:
            size: The buffer size in bytes
        """
        try:
            if not self._ensure_connection():
                raise Exception("Could not establish connection")

            # Clear the queue first (get all messages)
            while True:
                method_frame, _, _ = self.channel.basic_get(
                    queue="machine_buffer", auto_ack=True
                )
                if not method_frame:
                    break

            # Add the new buffer size
            self.channel.basic_publish(
                exchange="",
                routing_key="machine_buffer",
                body=str(size),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # make message persistent
                ),
            )
            self.logger.debug(f"Set current buffer size to {size} bytes")
        except Exception as e:
            self.logger.error(f"Error setting current buffer: {str(e)}")

    def on_data_arrive(self, size: int):
        """
        Update the buffer when new data arrives.

        Args:
            size: Size of the new data in bytes
        """
        try:
            current_buffer = self.get_current_buffer()
            new_buffer = current_buffer + size
            self.set_current_buffer(new_buffer)
            self.logger.debug(f"Buffer increased by {size} bytes to {new_buffer} bytes")
        except Exception as e:
            self.logger.error(f"Error handling data arrival: {str(e)}")

    def on_data_publish(self, size: int):
        """
        Update the buffer when data is published (removed from buffer).

        Args:
            size: Size of the published data in bytes
        """
        try:
            current_buffer = self.get_current_buffer()
            new_buffer = max(0, current_buffer - size)  # Ensure buffer doesn't go negative
            self.set_current_buffer(new_buffer)
            self.logger.debug(f"Buffer decreased by {size} bytes to {new_buffer} bytes")
        except Exception as e:
            self.logger.error(f"Error handling data publication: {str(e)}")

    def publish_stats_to_hq(self) -> bool:
        """
        Send buffer size to API endpoint with retry logic.
        
        Returns:
            True if report was successful, False otherwise
        """
        try:
            # Get current buffer
            buffer_size_bytes = self.get_current_buffer()
            
            # Prepare payload
            payload = {
                "machine_id": self.machine_id,
                "buffer": f"{buffer_size_bytes:.2f}",
                "updated_at": datetime.now(timezone.utc).isoformat(),
            }
            
            # Log current state
            self.logger.debug(f"Current buffer state: Total: {buffer_size_bytes:.2f} bytes")
            
            now = datetime.now(timezone.utc)
            date = now.strftime("%Y-%m-%d")
            filename = int(time.time() * 1000)
            
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
            self.logger.info("Machine stats publish SUCCESSFUL")
            return True
            
        except Exception as e:
            self.logger.error(f"Machine stats publish: Unexpected error: {e}")
            return False

    def start(self):
        """
        Start the machine stats service, including the background publisher thread.
        """
        try:
            self.logger.info("Starting MachineStats service...")
            self.is_running = True
            
            # Define the stats publisher loop
            def stats_publisher_loop():
                while self.is_running:
                    try:
                        self.publish_stats_to_hq()
                        time.sleep(self.stats_publish_interval)
                    except Exception as e:
                        self.logger.error(f"Error in stats publisher loop: {str(e)}")
                        time.sleep(self.publish_error_delay)
            
            # Create and start the thread
            self.stats_thread = threading.Thread(
                target=stats_publisher_loop, daemon=True
            )
            self.stats_thread.start()
            
            self.logger.info("MachineStats service started!")
            
        except Exception as e:
            self.logger.error(f"Error starting MachineStats service: {str(e)}")
            self.stop()
            raise

    def stop(self):
        """
        Stop the machine stats service and clean up resources.
        """
        self.is_running = False
        
        # Wait for thread to finish
        if (
            hasattr(self, "stats_thread")
            and self.stats_thread 
            and self.stats_thread.is_alive()
        ):
            self.stats_thread.join(timeout=5)
            
        # Clean up connection
        self.cleanup()
        
        self.logger.info("MachineStats service stopped")

    def cleanup(self):
        """
        Clean up resources, closing connections and channels.
        """
        if hasattr(self, "connection") and self.connection and self.connection.is_open:
            self.connection.close()
            self.logger.info("RabbitMQ connection closed")
        self.rabbit_mq.close()
 

    def is_healthy(self):
        """
        Check if the service is healthy.
        """
        return (
            self.is_running
            and hasattr(self, "connection")
            and self.connection
            and self.connection.is_open
            and self.rabbit_mq.is_healthy()
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
    """Example of how to use the MachineStats service"""
    print("Starting machine stats service example")
    
    # Create the service
    machine_stats = MachineStats()
    
    try:
        # Initialize with zero buffer
        machine_stats.set_current_buffer(0)
        
        # Simulate data arriving
        machine_stats.on_data_arrive(1024 * 1024)  # 1 MB
        print(f"Current buffer after data arrival: {machine_stats.get_current_buffer()} bytes")
        
        # Simulate publishing some data
        machine_stats.on_data_publish(512 * 1024)  # 512 KB
        print(f"Current buffer after publishing: {machine_stats.get_current_buffer()} bytes")
        
        # Publish stats to HQ
        machine_stats.publish_stats_to_hq()
        
        # Start the service for continuous monitoring
        machine_stats.start()
        
        # Let it run for a short while
        time.sleep(10)
        
    finally:
        # Clean up
        machine_stats.stop()
    
    print("Completed machine stats service example")


if __name__ == "__main__":
    main()