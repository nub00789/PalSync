import threading
import time


class LockManager:

    LOCK_TIMEOUT = 30

    def __init__(self):

        self._lock = threading.Lock()

        self.owner = None
        self.timestamp = 0

    def acquire(self, owner):

        with self._lock:

            now = time.time()

            if (
                self.owner is None
                or now - self.timestamp > self.LOCK_TIMEOUT
            ):

                self.owner = owner
                self.timestamp = now

                return True

            return self.owner == owner

    def release(self, owner):

        with self._lock:

            if self.owner == owner:

                self.owner = None
                self.timestamp = 0

                return True

            return False

    def heartbeat(self, owner):

        with self._lock:

            if self.owner == owner:

                self.timestamp = time.time()

                return True

            return False

    def status(self):

        with self._lock:

            return {
                "owner": self.owner,
                "locked": self.owner is not None,
                "expires_in": max(
                    0,
                    self.LOCK_TIMEOUT - (
                        time.time() - self.timestamp
                    )
                )
            }