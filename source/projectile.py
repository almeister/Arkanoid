from pygame.math import Vector2
from playercontroller import Movement


class Projectile:
    types = {'small': 'SmallBall.png'}
    FLIGHT_SPEED = 800
    LAUNCH_ANGLE_INCREMENT = 3

    def __init__(self, screen, sprite_sheet, sprite_name):
        self.screen = screen
        self.image = sprite_sheet.image_by_name(sprite_name)
        self.position = Vector2(0, 0)
        self.flight_speed = 0
        self.launch_angle = 90
        self.movement = Movement.IDLE
        self.direction = Vector2(0, 0)

    def get_size(self):
        return self.image.get_rect().size

    def set_position(self, position):
        self.position = position

    def fire(self):
        self.direction = Vector2(100, 0).rotate(self.launch_angle - 180)
        self.flight_speed = self.FLIGHT_SPEED

    def is_in_flight(self):
        return self.flight_speed > 0

    def update_launch_angle(self, movement):
        if self.movement == movement:
            if movement == Movement.LEFT:
                self.launch_angle = max(30, self.launch_angle - self.LAUNCH_ANGLE_INCREMENT)
            elif movement == Movement.RIGHT:
                self.launch_angle = min(150, self.launch_angle + self.LAUNCH_ANGLE_INCREMENT)
            else:
                self.reset_flight()
        else:
            self.reset_flight()

        self.movement = movement

    def reset_flight(self):
        self.movement = Movement.IDLE
        self.flight_speed = 0
        self.launch_angle = 90
        self.direction = Vector2(0, 0)

    def update(self, delta_t):
        if not self.screen.get_rect().contains((self.position, self.image.get_rect().size)):
            self.reset_flight()

        if self.is_in_flight():
            distance = self.flight_speed * delta_t / 1000
            self.position = self.position + distance * self.direction.normalize()

        rectangle = self.image.get_rect()
        rectangle.center = self.position
        self.screen.blit(self.image, rectangle)

