import operator
from collections import namedtuple


class PlayerPlatform:
    Position = namedtuple('Position', ['x', 'y'])
    platform_sprites = {'small': ((25, 190), (71, 22)), 'medium': ((25, 220), (138, 22)), 'large': ((25, 252), (204, 24))}

    def __init__(self, screen, sprite_sheet):
        # How to access screen as global singleton?
        self.screen = screen
        self.sprite_sheet = sprite_sheet
        self.position = self.Position(screen.get_rect().midbottom[0], screen.get_rect().midbottom[1] - 80)
        self.image = self.sprite_sheet.image_at(self.platform_sprites['large'])

    def move(self, delta):
        self.position = tuple(map(operator.add, self.position, (delta, 0)))

    def update(self):
        rectangle = self.image.get_rect()
        rectangle.center = self.position
        self.screen.blit(self.image, rectangle)
