import os
from pygame import image, error, Rect

from spritesheetdata import SpriteSheetData


class SpriteSheet:

    def __init__(self, sprites_path, filename):
        self.sprite_sheet_data = SpriteSheetData(os.path.join(sprites_path, filename))

        try:
            sheet_image_name = self.sprite_sheet_data.get_sheet_image_name()
            self.sheet = image.load(os.path.join(sprites_path, sheet_image_name)).convert_alpha()
        except error as e:
            print(f"Could not load sprite sheet: {sheet_image_name}.")
            raise SystemExit

    def image_by_name(self, name):
        frame = self.sprite_sheet_data.get_sprite(name)['frame']
        image_rect = Rect((frame['x'], frame['y']), (frame['w'], frame['h']))

        return self.image_at(image_rect)

    def image_at(self, rectangle):
        rect = Rect(rectangle)
        sprite = self.sheet.subsurface(rect)

        return sprite
