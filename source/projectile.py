import operator

from cartesiantypes import Point


class Projectile:
    types = {'small': 'SmallBall.png'}

    def __init__(self, screen, sprite_sheet, sprite_name):
        self.screen = screen
        self.image = sprite_sheet.image_by_name(sprite_name)
        self.position = Point(0, 0)  # TODO: replace positions with vectors?
        self.speed = 0

    def get_ball_size(self):
        return self.image.get_rect().size

    def set_position(self, position):
        self.position = position

    def fire(self):
        self.speed = 10

    def is_in_flight(self):
        return self.speed > 0

    # TODO: pass deltaT into update
    def update(self):
        self.position = tuple(map(operator.add, self.position, (0, -self.speed)))
        rectangle = self.image.get_rect()
        rectangle.center = self.position
        self.screen.blit(self.image, rectangle)

