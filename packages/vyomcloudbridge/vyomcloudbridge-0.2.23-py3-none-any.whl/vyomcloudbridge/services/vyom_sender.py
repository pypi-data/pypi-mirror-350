import threading
import time
from vyomcloudbridge.utils.configs import Configs
from vyomcloudbridge.utils.logger_setup import setup_logger
from vyomcloudbridge.senders.mav_sender import MavSender
from vyomcloudbridge.senders.mqtt_sender import MqttSender


class VyomSender:
    _instance = None
    _lock = threading.Lock()

    # def __new__(cls, *args, **kwargs):
    #     if cls._instance is None:
    #         with cls._lock:
    #             if cls._instance is None:
    #                 cls._instance = super(VyomSender, cls).__new__(cls)
    #                 print("VyomSender singleton initialized")
    #     print("Vyom Sender client service started")
    #     return cls._instance

    def __init__(
        self,
    ):
        try:
            """Initialize the Vyom Sender client"""
            if hasattr(self, "senders"):
                return
            self.logger = setup_logger(
                name=self.__class__.__module__ + "." + self.__class__.__name__,
                show_terminal=False,
            )
            self.logger.info("Starting VyomSender...")
            self.machine_config = Configs.get_machine_config()
            self.machine_id = self.machine_config.get("machine_id", "-") or "-"
            self.logger.info("Setting up all senders...")
            self.senders = {"mqtt": MqttSender(), "mavlink": MavSender()}
            self.logger.info("Setup of all senders Done!")
            # TODO, need to handle gcs, machine,
            self.network = {
                "s3": [
                    {"device_id": "s3", "channel": "mqtt"},
                ],
                "hq_1": [
                    {"device_id": "s3", "channel": "mqtt"},
                ],
                "gcs": [
                {"device_id": "gcs", "channel": "mavlink", "system_id": 255},
                ],
                "gcs2": [
                    {"device_id": "gcs2", "channel": "mqtt"},
                ],
                "machine_59": [
                    {"device_id": "machine_59", "channel": "mqtt"},
                ],
            }
            self.logger.info("VyomSender started sucessfully!")
        except Exception as e:
            self.logger.error("VyomSender starting failed")

    def send_message(self, message, message_type, destination_ids, data_source, topic):
        for destination_id in destination_ids:
            if self.network.get(destination_id, None) is not None and len(
                self.network.get(destination_id, None)
            ):
                try:
                    target_des_id = self.network.get(destination_id, None)[0].get(
                        "device_id", None
                    )
                    target_channel = self.network.get(destination_id, None)[0].get(
                        "channel", None
                    )
                    communicator = self.senders.get(target_channel)
                    communicator.send_message(
                        message,
                        message_type,
                        data_source,
                        target_des_id,
                        destination_id,
                        self.machine_id,
                        topic,
                    )
                    return True
                except Exception as e:
                    self.logger.error(
                        f"error in sending messages to {destination_id},  error: {str(e)}"
                    )
                    return False
            else:
                self.logger.error(
                    f"Error in sending messages to {destination_id}, no target found for teh destination"
                )
                return False

    def cleanup(self):
        """Call cleanup function of every sender instance and reset singleton"""
        for sender_name, sender_instance in self.senders.items():
            try:
                sender_instance.cleanup()
                self.logger.info(f"Successfully cleaned up {sender_name} sender")
            except Exception as e:
                self.logger.error(f"Error cleaning up {sender_name} sender: {str(e)}")

        # VyomSender._instance = None
        # self.logger.info("VyomSender cleanup completed and singleton reference reset")


# Initialize the singleton instance
# vyom_sender = VyomSender()


def main():
    """
    Main entry point for the queue worker service.
    """
    vyom_sender = VyomSender()
    try:
        time.sleep(10)
    except KeyboardInterrupt:
        pass
    finally:
        vyom_sender.cleanup()


if __name__ == "__main__":
    main()
