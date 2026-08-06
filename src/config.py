import json
from pathlib import Path

CONFIG_FILE = Path(__file__).parent.parent / "config.json"


class Config:

    def __init__(self):
        self.data = self.load()

    def load(self):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    @property
    def world_name(self):
        return self.data["world_name"]

    @property
    def players(self):
        return self.data["players"]

    @property
    def port(self):
        return self.data["port"]