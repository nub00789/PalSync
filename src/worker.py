from PySide6.QtCore import QObject, Signal
import time

from config import Config
from sync import SyncManager


class ServerWorker(QObject):

    finished = Signal(bool)
    status = Signal(str)

    def __init__(self, launcher):
        super().__init__()

        self.launcher = launcher

        cfg = Config()
        self.sync = SyncManager(cfg)

    def run(self):

        try:

            self.status.emit("Checking Syncthing...")

            while True:

                if not self.sync.health():

                    self.status.emit(
                        "Waiting for Syncthing..."
                    )

                    time.sleep(2)
                    continue

                if self.sync.completion() >= 100:

                    break

                self.status.emit(
                    "Waiting for world sync..."
                )

                time.sleep(2)

            self.status.emit(
                "Checking who is hosting..."
            )

            host = self.launcher.detector.get_online_host()

            if host is None:

                self.status.emit(
                    "No host online"
                )

                self.status.emit(
                    "Starting server..."
                )

            else:

                self.status.emit(
                    f'Connecting to {host["name"]}...'
                )

            self.launcher.play()

            self.status.emit(
                "Launching Palworld..."
            )

            self.finished.emit(True)

        except Exception as e:

            self.status.emit(str(e))
            self.finished.emit(False)


class StatusWorker(QObject):

    finished = Signal(dict)

    def __init__(self, detector, server):
        super().__init__()

        self.detector = detector
        self.server = server

    def run(self):

        host = self.detector.get_online_host()

        result = {
            "running": self.server.running(),
            "host": host
        }

        self.finished.emit(result)