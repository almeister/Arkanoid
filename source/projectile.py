import operator
from math import copysign

from pygame.math import Vector2


class Projectile:
    types = {'small': 'SmallBall.png'}
    LAUNCH_ANGLE_INCREMENT = 3

    def __init__(self, screen, sprite_sheet, sprite_name):
        self.screen = screen
        self.image = sprite_sheet.image_by_name(sprite_name)
        self.position = Vector2(0, 0)
        self.speed = 0
        self.launch_angle = 90
        self.delta = 0
        self.direction = Vector2(0, 0)

    def get_size(self):
        return self.image.get_rect().size

    def set_position(self, position):
        self.position = position

    def fire(self):
        self.direction = Vector2(100, 0).rotate(self.launch_angle - 180)
        self.speed = 10

    def is_in_flight(self):
        return self.speed > 0

    def update_launch_angle(self, delta):
        if delta == 0:
            self.reset()
        elif copysign(1, delta) == copysign(1, self.delta):
            if delta < 0:
                self.launch_angle = max(30, self.launch_angle - self.LAUNCH_ANGLE_INCREMENT)
            elif delta > 0:
                self.launch_angle = min(150, self.launch_angle + self.LAUNCH_ANGLE_INCREMENT)
        else:
            self.reset()

        self.delta = delta

    def reset(self):
        self.delta = 0
        self.speed = 0
        self.launch_angle = 90

    # TODO: pass deltaT into update
    def update(self):
        if not self.screen.get_rect().contains((self.position, self.image.get_rect().size)):
            self.reset()

        if self.speed > 0:
            self.position = self.position + self.speed * self.direction.normalize()
        rectangle = self.image.get_rect()
        rectangle.center = self.position
        self.screen.blit(self.image, rectangle)

