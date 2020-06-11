
class LevelData:

    def __init__(self, level_data):
        self.validate_level(level_data)
        self.level_data = level_data

    def get_grid(self):
        return self.level_data["grid"]

    def get_block_size(self):
        return self.level_data["block_size"]

    def get_blocks(self):
        return self.level_data["blocks"]

    def validate_level(self, level_data):
        assert "grid" in level_data
        assert "origin" in level_data["grid"]
        assert "w" in level_data["grid"]
        assert "h" in level_data["grid"]
        assert "blocks" in level_data

