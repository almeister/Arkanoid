import operator

from collections import namedtuple


class PlayerPlatform:
    Position = namedtuple('Position', ['x', 'y'])  # TODO: Remove typedef
    platform_sprites = {'small': 'SmallPlatform.png', 'medium': 'MediumPlatform.png', 'large': 'LargePlatform.png'}
    BOTTOM_SPACING = 80

    def __init__(self, screen, sprite_sheet):
        # TODO: Access screen as global singleton?
        self.screen = screen
        self.sprite_sheet = sprite_sheet
        self.position = self.Position(screen.get_rect().midbottom[0], screen.get_rect().midbottom[1] -
                                      self.BOTTOM_SPACING)
        self.image = self.sprite_sheet.image_by_name(self.platform_sprites['large'])

    def move(self, delta):
        self.position = tuple(map(operator.add, self.position, (delta, 0)))

    def update(self):
        rectangle = self.image.get_rect()
        rectangle.center = self.position
        self.screen.blit(self.image, rectangle)
