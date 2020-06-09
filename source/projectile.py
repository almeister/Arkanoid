from cartesiantypes import Point


class Projectile:
    types = {'small': 'SmallBall.png'}

    def __init__(self, screen, sprite_sheet, sprite_name):
        self.screen = screen
        self.image = sprite_sheet.image_by_name(sprite_name)
        self.position = Point(0, 0)
        self.speed = (0, 0)

    def get_ball_size(self):
        return self.image.get_rect().size

    def set_position(self, position):
        self.position = position

    def set_speed(self, speed):
        self.speed = speed

    def update(self):
        rectangle = self.image.get_rect()
        rectangle.center = self.position
        self.screen.blit(self.image, rectangle)

