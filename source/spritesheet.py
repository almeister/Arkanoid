import pygame


class SpriteSheet:

    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error as e:
            print(f"Could not load sprite sheet: {filename}.")
            raise SystemExit

    def image_at(self, rectangle, colorkey=None):
        # create an image
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size)
        # blit the rectangle from sprite sheet into image
        image.blit(self.sheet, image.get_rect(), rect)
        # return image

        return image
