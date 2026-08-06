from api_client import APIClient
from tailscale import Tailscale


class HostDetector:

    def __init__(self, players, port):
        self.players = players
        self.port = port
        self.tailscale = Tailscale()
        self.client = APIClient()

    def get_online_host(self):
        # Prefer a player who is actually hosting.
        for player in self.players:
            try:
                status = self.client.status(player["tailscale_ip"])

                if status and status.get("hosting"):
                    return {
                        "name": status.get("name", player["name"]),
                        "hostname": player["hostname"],
                        "ip": player["tailscale_ip"],
                        "ping": 0,
                    }

            except Exception:
                pass

        return None

    def get_online_players(self):

        online = []

        for player in self.players:
            try:
                if self.tailscale.online(player["hostname"]):
                    online.append(player)
            except Exception:
                pass

        return online

    def am_i_highest_priority(self, player_name):

        online = self.get_online_players()

        if not online:
            return True

        highest = min(
            online,
            key=lambda p: p.get("priority", 9999)
        )

        return highest["name"] == player_name