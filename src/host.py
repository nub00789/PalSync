import subprocess


class HostDetector:

    def __init__(self, players):
        self.players = players

    def ping(self, hostname):

        result = subprocess.run(
            ["ping", "-n", "1", hostname],
            capture_output=True,
            text=True
        )

        return result.returncode == 0

    def get_online_host(self):

        for player in self.players:

            if self.ping(player["hostname"]):
                return player["name"]

        return None