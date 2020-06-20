import operator

import pygame

from pygame.math import Vector2
from collisiondetector import CollisionDetector
from observer import Observer
from playercontroller import Movement
from spritegroup import SpriteGroupType


class Projectile(pygame.sprite.Sprite, Observer):
    types = {'small': 'SmallBall.png'}
    FLIGHT_SPEED = 800
    LAUNCH_ANGLE_INCREMENT = 3

    TEST_ANGLE = 50

    def __init__(self, screen, sprite_sheet, sprite_name, collision_detector):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.image = sprite_sheet.image_by_name(sprite_name)
        self.rect: pygame.Rect = self.image.get_rect()
        self.radius = self.rect.h / 2
        self.previous_rect: pygame.Rect = self.image.get_rect()
        self.flight_speed = 0
        self.launch_angle = self.TEST_ANGLE  # TODO: Set to 90
        self.movement = Movement.IDLE
        self.direction = Vector2(0, 0)  # TODO: change name to velocity
        collision_detector.add_listener(self)
        collision_detector.add_sprite(self)

    def on_observed(self, collision_detector: CollisionDetector) -> None:
        if collision_detector.collided_sprite_group_type == SpriteGroupType.BLOCKS:
            collided_sprite = collision_detector.collided_sprites[0]

            #  Find closest corner to projectile
            closest_distance = Vector2(self.screen.get_rect().size).magnitude()
            closest_corner = ""
            corners = {"topleft": Vector2(collided_sprite.rect.topleft),
                       "topright": Vector2(collided_sprite.rect.topright),
                       "bottomright": Vector2(collided_sprite.rect.bottomright),
                       "bottomleft": Vector2(collided_sprite.rect.bottomleft)}
            for key, corner in corners.items():
                distance = (Vector2(self.rect.center) - corner).magnitude()
                if distance < closest_distance:
                    closest_corner = key
                    closest_distance = distance

            #  Find closest side and reflect
            if closest_corner == "bottomright":
                surface_normal = Vector2(0, 1)
                collided_sprite_surface_point = Vector2(collided_sprite.rect.midbottom)
                intersection_comparison = self.projectile_intersects(collided_sprite_surface_point, surface_normal)
                if 0 < intersection_comparison <= 1:
                    # Projectile hit the bottom of collided sprite
                    self.direction = self.direction.reflect(surface_normal)
                    # Move projectile back outside the rectangle
                    self.rect.centery = corners[closest_corner].y + self.radius
                    return

                surface_normal = Vector2(1, 0)
                collided_sprite_surface_point = Vector2(collided_sprite.rect.midright)
                intersection_comparison = self.projectile_intersects(collided_sprite_surface_point, surface_normal)
                if 0 < intersection_comparison <= 1:
                    # Projectile hit right of collided sprite
                    self.direction = self.direction.reflect(surface_normal)
                    # Move projectile back outside the rectangle
                    self.rect.centerx = corners[closest_corner].x + self.radius
                    return

            elif closest_corner == "topright":
                surface_normal = Vector2(1, 0)
                collided_sprite_surface_point = Vector2(collided_sprite.rect.midright)
                intersection_comparison = self.projectile_intersects(collided_sprite_surface_point, surface_normal)
                if 0 < intersection_comparison <= 1:
                    # Projectile hit right side of collided sprite
                    self.direction = self.direction.reflect(surface_normal)
                    # Move projectile back outside the rectangle
                    self.rect.centerx = corners[closest_corner].x + self.radius
                    return

                surface_normal = Vector2(0, -1)
                collided_sprite_surface_point = Vector2(collided_sprite.rect.midtop)
                intersection_comparison = self.projectile_intersects(collided_sprite_surface_point, surface_normal)
                if 0 < intersection_comparison <= 1:
                    # Projectile hit top of collided sprite
                    self.direction = self.direction.reflect(surface_normal)
                    # Move projectile back outside the rectangle
                    self.rect.centery = corners[closest_corner].y - self.radius
                    return

    def projectile_intersects(self, collided_sprite_surface_point, surface_normal):
        projectile_edge_point = Vector2(self.rect.center) - self.radius * surface_normal
        previous_projectile_edge_point = Vector2(self.previous_rect.center) - self.radius * surface_normal
        projectile_collision_path = projectile_edge_point - previous_projectile_edge_point
        dot1 = surface_normal.dot(collided_sprite_surface_point - previous_projectile_edge_point)
        dot2 = surface_normal.dot(projectile_collision_path)
        intersection_comparison = dot1 / dot2
        return intersection_comparison

    def get_size(self):
        return self.image.get_rect().size

    def set_position(self, position):
        self.rect.center = position

    def fire(self):
        if not self.is_in_flight():
            self.direction = Vector2(100, 0).rotate(self.launch_angle - 180)
            self.flight_speed = self.FLIGHT_SPEED

    def is_in_flight(self):
        return self.flight_speed > 0

    def update_launch_angle(self, movement):
        pass
        # if self.movement == movement:
        #     if movement == Movement.LEFT:
        #         self.launch_angle = max(30, self.launch_angle - self.LAUNCH_ANGLE_INCREMENT)
        #     elif movement == Movement.RIGHT:
        #         self.launch_angle = min(150, self.launch_angle + self.LAUNCH_ANGLE_INCREMENT)
        #     else:
        #         self.reset_flight()
        # else:
        #     self.reset_flight()
        #
        # self.movement = movement

    def reset_flight(self):
        self.movement = Movement.IDLE
        self.flight_speed = 0
        self.launch_angle = self.TEST_ANGLE  # TODO: Set to 90
        self.direction = Vector2(0, 0)

    def any_collisions(self, group):
        return pygame.sprite.spritecollideany(self, group)

    def update(self, delta_t, group):
        self.previous_rect = self.rect.copy()
        if not self.screen.get_rect().contains(self.rect):
            self.reset_flight()
        elif self.is_in_flight():
            distance = self.flight_speed * delta_t / 1000
            self.rect.center = self.rect.center + distance * self.direction.normalize()

        self.screen.blit(self.image, self.rect)
