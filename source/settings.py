import os


class Settings:

    def __init__(self):
        self.screen_width, self.screen_height = 1200, 800
        self.bg_color = (23, 225, 225)
        self.project_path = os.path.dirname("../")
        self.assets_path = os.path.join(self.project_path, "assets")
        self.sprites_path = os.path.join(self.assets_path, "sprites")
        self.levels_path = os.path.join(self.assets_path, "levels")
