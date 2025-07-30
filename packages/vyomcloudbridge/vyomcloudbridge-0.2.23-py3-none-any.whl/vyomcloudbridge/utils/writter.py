# writer.py
from vyomcloudbridge.utils.shared_memory import SharedMemoryUtil
import time


if __name__ == "__main__":
    data_to_set = {"ack": 1, "status": "ok"}

    shared_mem = SharedMemoryUtil()
    shared_mem.set_data(data_to_set)
    print("Data written:", data_to_set)