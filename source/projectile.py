from typing import Tuple

from pygame.math import Vector2
from pygame.sprite import Sprite

from collisiondetector import CollisionDetector
from gameevent import BlockHitEvent
from observer import Observer
from spritegroup import SpriteGroupType


class Projectile(Sprite, Observer):
    types = {'small': 'SmallBall.png'}
    FLIGHT_SPEED = 500

    def __init__(self, screen, sprite_sheet, sprite_name, collision_detector, event_bus):
        Sprite.__init__(self)
        self.screen = screen
        self.image = sprite_sheet.image_by_name(sprite_name)
        self.rect = self.image.get_rect()
        self.radius = self.rect.h / 2
        self.hidden = False
        self.previous_rect = self.image.get_rect()
        self.flight_speed = 0
        self.velocity = Vector2(0, 0)
        collision_detector.add_listener(self)
        self.event_bus = event_bus

    def on_observed(self, collision_detector: CollisionDetector) -> None:
        sprite_group = collision_detector.collided_sprite_group
        if (sprite_group.group_type == SpriteGroupType.BLOCKS or
                sprite_group.group_type == SpriteGroupType.BOUNDARIES or
                sprite_group.group_type == SpriteGroupType.PLATFORM):
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
                        if sprite_group.group_type == SpriteGroupType.BLOCKS:
                            event = BlockHitEvent(collided_sprite, collided_sprite.rect.midbottom)
                            self.event_bus.publish(event)
                        return

    def projectile_intersects(self, surface_test_point, surface_normal):
        # Line-plane intersection algorithm based on dot-product comparison.
        # https://pygamerist.blogspot.com/2020/06/arkanoid-and-collision-detection.html
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

    def set_position(self, position):
        self.rect.center = position

    def launch(self, launch_angle):
        if not self.in_flight():
            self.velocity = Vector2(1, 0).rotate(launch_angle - 180)
            self.flight_speed = self.FLIGHT_SPEED

    def in_flight(self):
        return self.flight_speed > 0

    def reset_flight(self):
        self.flight_speed = 0
        self.velocity = Vector2(0, 0)

    def hide(self):
        self.hidden = True

    def show(self):
        self.hidden = False

    def update(self, delta_t):
        if not self.hidden:
            self.previous_rect = self.rect.copy()
            if self.in_flight():
                distance = self.flight_speed * delta_t / 1000
                self.rect.center = self.rect.center + distance * self.velocity.normalize()

            self.screen.blit(self.image, self.rect)


class TestSurface:

    def __init__(self, name: str, surface_normal: Tuple[int, int], surface_test_point: Tuple[int, int]):
        self.name = name
        self.surface_normal = Vector2(surface_normal)
        self.surface_test_point = Vector2(surface_test_point)

