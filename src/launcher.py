import os
import subprocess
import time

from host import HostDetector
from server import ServerManager


class Launcher:

    def __init__(self, config):

        self.cfg = config

        self.detector = HostDetector(
            config.players,
            config.port
        )

        self.server = ServerManager(
            config.server_path,
            config.port
        )

    def play(self):

        # Someone is already hosting
        host = self.detector.get_online_host()

        if host is not None:

            self.launch_game()

            return host

        # Nobody is hosting.
        # If we're the highest-priority online player,
        # become the host immediately.
        if self.detector.am_i_highest_priority(
            self.cfg.player_name
        ):

            self.server.start()

            if not self.server.wait_until_ready():

                raise RuntimeError(
                    "Server failed to start."
                )

            self.launch_game()

            return self.detector.get_online_host()

        # Wait for the higher-priority player.
        print("Waiting for higher-priority host...")

        for _ in range(self.cfg.host_wait_timeout):

            host = self.detector.get_online_host()

            if host is not None:

                self.launch_game()

                return host

            time.sleep(1)

        print("Host timeout. Becoming host...")

        self.server.start()

        if not self.server.wait_until_ready():

            raise RuntimeError(
                "Server failed to start."
            )

        self.launch_game()

        return self.detector.get_online_host()

    def launch_game(self):

        exe = os.path.join(
            self.cfg.steam_path,
            "Palworld.exe"
        )

        if not os.path.exists(exe):

            exe = os.path.join(
                self.cfg.steam_path,
                "Pal",
                "Binaries",
                "Win64",
                "Palworld-Win64-Shipping.exe"
            )

        if not os.path.exists(exe):

            raise FileNotFoundError(
                "Couldn't find Palworld executable."
            )

        subprocess.Popen(exe)

        return True