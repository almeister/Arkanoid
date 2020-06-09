import operator

from collections import namedtuple

from projectile import Projectile


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
        self.projectile = Projectile(self.screen, self.sprite_sheet, Projectile.types["small"])

    def get_position(self):
        return self.position

    def move(self, delta):
        self.position = tuple(map(operator.add, self.position, (delta, 0)))
        projectile_size = self.projectile.get_ball_size()
        projectile_position = self.Position(self.position[0], self.position[1] - projectile_size[0])
        self.projectile.set_position(projectile_position)

    def update(self):
        rectangle = self.image.get_rect()
        rectangle.center = self.position
        self.screen.blit(self.image, rectangle)
        self.projectile.update()
