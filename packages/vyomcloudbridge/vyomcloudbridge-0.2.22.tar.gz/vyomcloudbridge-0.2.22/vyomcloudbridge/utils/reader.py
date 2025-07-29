# reader.py
from vyomcloudbridge.utils.shared_memory import SharedMemoryUtil
import time

def get_ack_data_received():
    shared_mem = SharedMemoryUtil()
    data = shared_mem.get_data()
    return data.get("mavlink_ack_data", {})

if __name__ == "__main__":
    while True:
        ack_data = get_ack_data_received()
        print("[Reader] Current shared memory data:", ack_data)
        time.sleep(1)
