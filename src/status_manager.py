import threading
import time

from config import Config
from server import ServerManager
from sync import SyncManager
import status_store


class StatusManager:

    def __init__(self):

        self.cfg = Config()

        self.server = ServerManager(
            self.cfg.server_path,
            self.cfg.port
        )

        self.sync = SyncManager(self.cfg)

        self.running = False
        self.thread = None

    def start(self):

        if self.running:
            return

        self.running = True

        self.thread = threading.Thread(
            target=self.loop,
            daemon=True,
            name="StatusManager"
        )

        self.thread.start()

    def stop(self):

        self.running = False

    def loop(self):

        while self.running:

            try:

                status_store.update(
                    name=self.cfg.player_name,
                    hosting=self.server.running(),
                    running=self.server.running(),
                    sync=self.sync.completion(),
                )

            except Exception as e:
                print(f"StatusManager Error: {e}")

            time.sleep(1)