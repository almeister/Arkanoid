import pygame

from typing import Tuple
from pygame.math import Vector2
from collisiondetector import CollisionDetector
from observer import Observer
from playercontroller import Movement
from spritegroup import SpriteGroupType


class Projectile(pygame.sprite.Sprite, Observer):
    types = {'small': 'SmallBall.png'}
    FLIGHT_SPEED = 800
    LAUNCH_ANGLE_INCREMENT = 3

    def __init__(self, screen, sprite_sheet, sprite_name, collision_detector):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.image = sprite_sheet.image_by_name(sprite_name)
        self.rect: pygame.Rect = self.image.get_rect()
        self.radius = self.rect.h / 2
        self.previous_rect: pygame.Rect = self.image.get_rect()
        self.flight_speed = 0
        self.launch_angle = 90
        self.movement = Movement.IDLE
        self.velocity = Vector2(0, 0)  # TODO: change name to velocity
        collision_detector.add_listener(self)
        collision_detector.add_sprite(self)

    def on_observed(self, collision_detector: CollisionDetector) -> None:
        if collision_detector.collided_sprite_group_type == SpriteGroupType.BLOCKS:
            for collided_sprite in collision_detector.collided_sprites:
                test_surfaces = [
                    TestSurface("top", (0, -1), collided_sprite.rect.midtop),
                    TestSurface("right", (1, 0), collided_sprite.rect.midright),
                    TestSurface("bottom", (0, 1), collided_sprite.rect.midbottom),
                    TestSurface("left", (-1, 0), collided_sprite.rect.midleft)
                ]

                for test_surface in test_surfaces:
                    if self.projectile_intersects(test_surface.surface_test_point, test_surface.surface_normal):
                        self.reflect(test_surface.surface_normal)
                        return

    def projectile_intersects(self, surface_test_point, surface_normal):
        # Line-plane intersection algorithm based on dot-product comparison. For more info:
        # https://www.gamedev.net/tutorials/programming/math-and-physics/practical-use-of-vector-math-in-games-r2968/
        projectile_edge_point = Vector2(self.rect.center) - self.radius * surface_normal
        previous_projectile_edge_point = Vector2(self.previous_rect.center) - self.radius * surface_normal
        projectile_collision_path = projectile_edge_point - previous_projectile_edge_point
        dot1 = surface_normal.dot(surface_test_point - previous_projectile_edge_point)
        dot2 = surface_normal.dot(projectile_collision_path)

        if dot2 == 0.0:
            return False

        return 0 < dot1 / dot2 <= 1

    def reflect(self, surface_normal):
        self.velocity = self.velocity.reflect(surface_normal)
        self.rect.center += self.radius * surface_normal

    def get_size(self):
        return self.image.get_rect().size

    def set_position(self, position):
        self.rect.center = position

    def fire(self):
        if not self.is_in_flight():
            self.velocity = Vector2(100, 0).rotate(self.launch_angle - 180)
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
        self.velocity = Vector2(0, 0)

    def any_collisions(self, group):
        return pygame.sprite.spritecollideany(self, group)

    def update(self, delta_t, group):
        self.previous_rect = self.rect.copy()
        if not self.screen.get_rect().contains(self.rect):
            self.reset_flight()
        elif self.is_in_flight():
            distance = self.flight_speed * delta_t / 1000
            self.rect.center = self.rect.center + distance * self.velocity.normalize()

        self.screen.blit(self.image, self.rect)


class TestSurface:

    def __init__(self, name: str, surface_normal: Tuple[int, int], surface_test_point: Tuple[int, int]):
        self.name = name
        self.surface_normal = Vector2(surface_normal)
        self.surface_test_point = Vector2(surface_test_point)

