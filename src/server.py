import subprocess
import os
import time
import psutil


class ServerManager:

    def __init__(self, server_path, port=8211):
        self.server_path = server_path
        self.port = port
        self.process = None

    # ---------------------------------------
    # Check if Palworld server is already running
    # ---------------------------------------

    def running(self):

        for process in psutil.process_iter(["name"]):

            try:

                name = process.info["name"]

                if name and "PalServer-Win64-Shipping" in name:
                    return True

            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        return False

    # ---------------------------------------
    # Start Server
    # ---------------------------------------

    def start(self):

        if self.running():
            return True

        folder = os.path.dirname(self.server_path)

        self.process = subprocess.Popen(
            self.server_path,
            cwd=folder
        )

        return True

    # ---------------------------------------
    # Wait until running
    # ---------------------------------------

    def wait_until_ready(self, timeout=60):

        start = time.time()

        while time.time() - start < timeout:

            if self.running():
                return True

            time.sleep(0.5)

        return False

    # ---------------------------------------
    # Stop server
    # ---------------------------------------

    def stop(self):

        for process in psutil.process_iter(["pid", "name"]):

            try:

                name = process.info["name"]

                if name and (
                    "PalServer-Win64-Shipping" in name
                    or name == "PalServer.exe"
                ):

                    process.terminate()

            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        self.process = None