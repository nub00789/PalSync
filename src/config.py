import json
from pathlib import Path

CONFIG_PATH = Path(__file__).parent.parent / "config.json"


class Config:

    def __init__(self):
        self.reload()

    def reload(self):

        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            self.data = json.load(f)

    @property
    def player_name(self):
        return self.data["player_name"]

    @property
    def world_name(self):
        return self.data["world_name"]

    @property
    def port(self):
        return self.data["port"]

    @property
    def query_port(self):
        return self.data["query_port"]

    @property
    def host_wait_timeout(self):
        return self.data["host_wait_timeout"]

    @property
    def players(self):
        return self.data["players"]

    @property
    def steam_path(self):
        return self.data["steam_path"]

    @property
    def server_path(self):
        return self.data["server_path"]

    @property
    def save_path(self):
        return self.data["save_path"]

    @property
    def syncthing(self):
        return self.data["syncthing"]

    def save(self):

        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(
                self.data,
                f,
                indent=4
            )

    def set(self, key, value):

        self.data[key] = value
        self.save()