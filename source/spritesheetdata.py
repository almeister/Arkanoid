import json


class SpriteSheetData:

    def __init__(self, file_name):
        file_json = open(file_name, "r").read()
        data = json.loads(file_json)
        self.sheet_image_name = data["meta"]["image"]
        self.frames = data["frames"]

    def get_sheet_image_name(self):
        return self.sheet_image_name

    def get_sprite(self, sprite_name):
        return self.frames[sprite_name]
