from tailscale import Tailscale


class HostDetector:

    def __init__(self, players, port):
        self.players = players
        self.port = port
        self.tailscale = Tailscale()

    def get_online_host(self):

        # Prefer Yusuf if online
        for player in self.players:

            if (
                player["name"].lower() == "yusuf"
                and self.tailscale.online(player["hostname"])
            ):

                return {
                    "name": player["name"],
                    "hostname": player["hostname"],
                    "ip": player["tailscale_ip"],
                    "ping": 0
                }

        # Otherwise check everyone else
        for player in self.players:

            if player["name"].lower() == "yusuf":
                continue

            if self.tailscale.online(player["hostname"]):

                return {
                    "name": player["name"],
                    "hostname": player["hostname"],
                    "ip": player["tailscale_ip"],
                    "ping": 0
                }

        return None