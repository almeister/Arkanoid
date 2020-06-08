
class LevelData:

    def __init__(self, level_data):
        self.validate_level(level_data)
        self.level_data = level_data

    def get_grid(self):
        return self.level_data["grid"]

    def get_blocks(self):
        return self.level_data["blocks"]

    def validate_level(self, level_data):
        # TODO: Assert on bad level data
        return True
