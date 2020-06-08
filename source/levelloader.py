import json
import os

from leveldata import LevelData


class LevelLoader:

    def __init__(self, levels_folder):
        self.levels_folder = levels_folder

    def load_level(self, level_number):
        file_json = open(os.path.join(self.levels_folder, f"level_{level_number}.json"), "r").read()
        level_data = json.loads(file_json)

        return LevelData(level_data)
