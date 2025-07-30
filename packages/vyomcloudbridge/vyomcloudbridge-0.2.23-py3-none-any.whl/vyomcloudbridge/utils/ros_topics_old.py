import json
import time
# import rclpy
# import os
# import random
# from rclpy.node import Node


class ROSTopic:
    def init(self):
        try:
            # rclpy.init(args=None)
            pass
        except Exception as e:
            self.logger.warning(f"Failed to initialize ROS: {e}")
        # self.topic_node = Node("topic_discoverer")

    def serialize_topic_list(self):
        topic_name = self.topic_node.get_topic_names_and_types()

        # creating a dictionary with topic name as key and topic type as value
        topic_dict = {
            topic_name: topic_type[0] for topic_name, topic_type in topic_name
        }

        # convert to json
        serialised_topic = json.dumps(topic_dict)

        print(f"Topics in json: {serialised_topic}")

        return serialised_topic

    def cleanup(self):
        pass
        # rclpy.shutdown()


if __name__ == "__main__":
    topics_discoverer = ROSTopic()
    topic_list = topics_discoverer.serialize_topic_list()
    topics_discoverer.cleanup()
