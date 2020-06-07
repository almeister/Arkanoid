import os
import pygame

from spritesheetdata import SpriteSheetData


class SpriteSheet:

    def __init__(self, sprites_path, filename):
        self.sprite_sheet_data = SpriteSheetData(os.path.join(sprites_path, filename))

        try:
            sheet_image_name = self.sprite_sheet_data.get_sheet_image_name()
            self.sheet = pygame.image.load(os.path.join(sprites_path, sheet_image_name)).convert_alpha()
        except pygame.error as e:
            print(f"Could not load sprite sheet: {sheet_image_name}.")
            raise SystemExit

    def image_by_name(self, name):
        frame = self.sprite_sheet_data.get_sprite(name)['frame']
        image_rect = pygame.Rect((frame['x'], frame['y']), (frame['w'], frame['h']))

        return self.image_at(image_rect)

    def image_at(self, rectangle):
        rect = pygame.Rect(rectangle)
        image = self.sheet.subsurface(rect)

        return image
