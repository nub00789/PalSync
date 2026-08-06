from api_client import APIClient
from tailscale import Tailscale


class HostDetector:

    def __init__(self, players, port):
        self.players = players
        self.port = port
        self.tailscale = Tailscale()
        self.client = APIClient()

    def get_online_host(self):

        # First preference:
        # Find someone whose PalSync reports hosting=True.
        for player in self.players:

            try:

                status = self.client.status(player["tailscale_ip"])

                if status and status.get("hosting"):

                    return {
                        "name": status.get("name", player["name"]),
                        "hostname": player["hostname"],
                        "ip": player["tailscale_ip"],
                        "ping": 0
                    }

            except Exception:
                pass

        # Fallback:
        # If nobody reports hosting, return the first online PC.
        for player in self.players:

            try:

                if self.tailscale.online(player["hostname"]):

                    return {
                        "name": player["name"],
                        "hostname": player["hostname"],
                        "ip": player["tailscale_ip"],
                        "ping": 0
                    }

            except Exception:
                pass

        return None