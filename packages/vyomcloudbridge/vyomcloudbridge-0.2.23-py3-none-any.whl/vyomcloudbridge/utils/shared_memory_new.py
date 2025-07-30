# In a new shared file (e.g., shared_memory_utils.py)
import json
import pickle
from multiprocessing import shared_memory
import threading
from vyomcloudbridge.utils.logger_setup import setup_logger

logger = setup_logger(name=__name__, show_terminal=False)

class SharedMemoryUtil:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(SharedMemoryUtil, cls).__new__(cls)
                    cls._instance.__init__()
                    print("SharedMemoryUtil initialized")
        return cls._instance
    
    def __init__(self):
        pass

    # TODO not sure if this is needed
    def _ensure_shared_memory(self, data_key): # Ensure shared memory exists for the given key
        # Define initial empty dict
        init_data = {}
        serialized_data = pickle.dumps(init_data)

        # Size with some buffer for growth
        buffer_size = max(len(serialized_data) * 10, 10240)  # At least 10KB

        try:
            # Try to attach to existing shared memory
            self.shm = shared_memory.SharedMemory(name=data_key)
            # If it exists, don't initialize it
        except FileNotFoundError:
            # Create new shared memory if it doesn't exist
            self.shm = shared_memory.SharedMemory(
                name=data_key, create=True, size=buffer_size
            )
            # Initialize with empty dict
            self.shm.buf[: len(serialized_data)] = serialized_data
            # Store the length
            length_bytes = len(serialized_data).to_bytes(4, byteorder="little")
            self.shm.buf[buffer_size - 4 : buffer_size] = length_bytes

    def get_data(self, data_key): # get data from shared memory for a given key
        try:
            self._ensure_shared_memory(data_key)
            # TODO <update this>
            # set the data_key to the shared memory
            # <TODO>
            return True
        except FileNotFoundError as e:   

            # If it doesn't exist, return None or raise an error
            return None

    def set_data(self, data_key, data):
        # make lock for the current key only not for all keys
        self._ensure_shared_memory(data_key)
        try:
            # Try to create new shared memory
            shared_memory.SharedMemory(name=data_key, create=True, size=1)
        except FileExistsError:
            return
            
            
            


    def cleanup(self):
        self.shm.close()
        # Unlink only when the application is shutting down
        # to avoid removing shared memory while other processes are using it
        self.shm.unlink()
