import json

from leveldata import LevelData


class LevelLoader:

    def __init__(self):
        pass

    def load_level(self, file_path):
        file_json = open(file_path, "r").read()
        level_data = json.loads(file_json)

        return LevelData(level_data)
