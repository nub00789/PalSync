import xml.etree.ElementTree as ET
from pathlib import Path

import requests


class SyncManager:

    def __init__(self, config):

        self.url = config.syncthing["url"]
        self.folder = config.syncthing["folder_id"]

        self.headers = {
            "X-API-Key": self.read_api_key()
        }

    def read_api_key(self):

        config_path = (
            Path.home()
            / "AppData"
            / "Local"
            / "Syncthing"
            / "config.xml"
        )

        tree = ET.parse(config_path)

        root = tree.getroot()

        gui = root.find("gui")

        if gui is None:
            raise RuntimeError(
                "Couldn't find Syncthing GUI settings."
            )

        api = gui.find("apikey")

        if api is None:
            raise RuntimeError(
                "Couldn't find Syncthing API key."
            )

        return api.text.strip()

    def health(self):

        try:

            r = requests.get(
                f"{self.url}/rest/noauth/health",
                timeout=2
            )

            return (
                r.json()["status"] == "OK"
            )

        except Exception:

            return False

    def completion(self):

        try:

            r = requests.get(
                f"{self.url}/rest/db/completion",
                params={
                    "folder": self.folder
                },
                headers=self.headers,
                timeout=2
            )

            data = r.json()

            return round(
                data.get("completion", 100)
            )

        except Exception:

            return 0

    def status(self):

        try:

            r = requests.get(
                f"{self.url}/rest/db/status",
                params={
                    "folder": self.folder
                },
                headers=self.headers,
                timeout=2
            )

            return r.json()

        except Exception:

            return {}