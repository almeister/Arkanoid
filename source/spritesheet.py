import pygame


class SpriteSheet:

    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert_alpha()
        except pygame.error as e:
            print(f"Could not load sprite sheet: {filename}.")
            raise SystemExit

    def image_at(self, rectangle, colorkey=None):
        rect = pygame.Rect(rectangle)
        image = self.sheet.subsurface(rect)

        return image
