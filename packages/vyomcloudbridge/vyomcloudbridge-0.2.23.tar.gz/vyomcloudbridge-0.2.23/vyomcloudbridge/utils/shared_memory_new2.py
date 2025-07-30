import pickle
from typing import Any
from multiprocessing import shared_memory, Lock
import threading


class SharedMemoryUtil:
    _instance = None
    _global_lock = threading.Lock()
    _key_locks = {}

    def __new__(cls):
        if cls._instance is None:
            with cls._global_lock:
                if cls._instance is None:
                    cls._instance = super(SharedMemoryUtil, cls).__new__(cls)
                    cls._instance._key_locks = {}
        return cls._instance

    def __init__(self):
        self.default_size = 1024 * 1024  # Default size of 1MB for shared memory

    def _get_lock(self, key):  # private method
        if key not in self._key_locks:
            with self._global_lock:
                if key not in self._key_locks:
                    self._key_locks[key] = Lock()
        return self._key_locks[key]

    def get_lock(self, key):  # public method
        """Get a lock for a given key, create if it doesn't exist."""
        if not key or not isinstance(key, str):
            raise ValueError("Key must be non empty string")
        if not key.startswith("vyomcloudbridge_"):
            key = f"vyomcloudbridge_{key}"

        if key not in self._key_locks:
            with self._global_lock:
                if key not in self._key_locks:
                    self._key_locks[key] = Lock()
        return self._key_locks[key]

    def _get_shm(self, key, size=None):
        """Get shared memory by key, create if it doesn't exist."""
        try:
            return shared_memory.SharedMemory(name=key)
        except FileNotFoundError:
            if size is not None:
                return shared_memory.SharedMemory(name=key, create=True, size=size)
            else:
                return shared_memory.SharedMemory(name=key, create=True, size=size)

    def set_data(self, key: str, value: Any):
        """Set data in shared memory with a given key."""
        if not key or not isinstance(key, str):
            raise ValueError("Key must be non empty string")
        if not key.startswith("vyomcloudbridge_"):
            key = f"vyomcloudbridge_{key}"

        lock = self._get_lock(key)
        with lock:
            data_bytes = pickle.dumps(value)
            shm = self._get_shm(key, size=len(data_bytes))
            if shm.size < len(data_bytes):
                shm.close()
                shm.unlink()
                shm = shared_memory.SharedMemory(
                    name=key, create=True, size=len(data_bytes)
                )
            shm.buf[: len(data_bytes)] = data_bytes
            shm.close()
            return True

    def get_data(self, key: str):
        """Get data from shared memory by key."""
        if not key or not isinstance(key, str):
            raise ValueError("Key must be non empty string")
        if not key.startswith("vyomcloudbridge_"):
            key = f"vyomcloudbridge_{key}"

        shm = self._get_shm(key)
        if shm is None:
            return None
        try:
            data = bytes(shm.buf[:])
            return pickle.loads(data)
        finally:
            shm.close()

    def delete_data(self, key: str):
        """Delete data from shared memory by key."""
        if not key or not isinstance(key, str):
            raise ValueError("Key must be non empty string")
        if not key.startswith("vyomcloudbridge_"):
            key = f"vyomcloudbridge_{key}"

        lock = self._get_lock(key)
        with lock:
            shm = self._get_shm(key)
            if shm:
                shm.close()
                shm.unlink()
                return True
            return False


if __name__ == "__main__":
    # Example 1
    sm_util = SharedMemoryUtil()
    success = sm_util.set_data("my_key", {"count": 42, "status": "active"})
    print("Set success:", success)

    # Example 2
    sm_util = SharedMemoryUtil()
    data = sm_util.get_data("my_key")
    print("Retrieved data:", data)

    # Example 3
    sm_util = SharedMemoryUtil()

    # Step 1: Get existing data
    lock = sm_util.get_lock("my_key")
    with lock:
        data = sm_util.get_data("my_key")
        if data:
            data["count"] += 1

        # Step 2: Set updated data
        sm_util.set_data("my_key", data)
        print("Updated data:", data)
