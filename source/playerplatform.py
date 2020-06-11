import operator

from cartesiantypes import Point
from projectile import Projectile
from playercontroller import Movement


class PlayerPlatform:
    platform_sprites = {'small': 'SmallPlatform.png', 'medium': 'MediumPlatform.png', 'large': 'LargePlatform.png'}
    BOTTOM_SPACING = 80
    MOVEMENT_SPEED = 900

    def __init__(self, screen, sprite_sheet):
        self.screen = screen
        self.sprite_sheet = sprite_sheet
        self.position = Point(screen.get_rect().midbottom[0], screen.get_rect().midbottom[1] -
                              self.BOTTOM_SPACING)
        self.image = self.sprite_sheet.image_by_name(self.platform_sprites['small'])
        self.projectile = Projectile(self.screen, self.sprite_sheet, Projectile.types["small"])

    def get_position(self):
        return self.position

    def move(self, movement, delta_t):
        distance = self.MOVEMENT_SPEED * delta_t / 1000
        if movement == Movement.LEFT:
            distance = -distance
        elif movement == Movement.RIGHT:
            pass
        else:
            distance = 0

        self.position = tuple(map(operator.add, self.position, (distance, 0)))

        if not self.projectile.is_in_flight():
            projectile_size = self.projectile.get_size()
            projectile_position = Point(self.position[0], self.position[1] - projectile_size[0])
            self.projectile.update_launch_angle(movement)
            self.projectile.set_position(projectile_position)

    def fire(self):
        self.projectile.fire()

    def update(self, delta_t):
        rectangle = self.image.get_rect()
        rectangle.center = self.position
        self.screen.blit(self.image, rectangle)
        self.projectile.update(delta_t)
