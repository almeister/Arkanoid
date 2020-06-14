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

    def __init__(self, screen, sprite_sheet, sprite_name, collision_detector):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.image = sprite_sheet.image_by_name(sprite_name)
        self.rect = self.image.get_rect()
        self.previous_rect = self.image.get_rect()
        self.flight_speed = 0
        self.launch_angle = 45 # TODO: Set to 90
        self.movement = Movement.IDLE
        self.direction = Vector2(0, 0)
        collision_detector.add_listener(self)
        collision_detector.add_sprite(self)

    def on_observed(self, collision_detector: CollisionDetector) -> None:
        if collision_detector.collided_sprite_group_type == SpriteGroupType.BLOCKS:
            collided_sprite = collision_detector.collided_sprites[0]

            # TODO: Fix arguments warning
            prev_pos_to_collided_corner = Vector2(tuple(map(operator.sub, self.previous_rect.topleft,
                                                            collided_sprite.rect.bottomright)))
            current_pos_to_previous_pos = Vector2(tuple(map(operator.sub, self.rect.topleft,
                                                            self.previous_rect.topleft)))
            if prev_pos_to_collided_corner.y <= 0:
                # Projectile hit right of collided sprite
                self.direction = self.direction.reflect(Vector2(1, 0))
            elif prev_pos_to_collided_corner.x <= 0:
                # Projectile hit the bottom of collided sprite
                self.direction = self.direction.reflect(Vector2(0, -1))
            else:
                approach_ratio = abs((current_pos_to_previous_pos.y / current_pos_to_previous_pos.x) / \
                                     (prev_pos_to_collided_corner.y / prev_pos_to_collided_corner.x))
                if approach_ratio < 1:
                    # Projectile hit right of collided sprite
                    self.direction = self.direction.reflect(Vector2(1, 0))
                elif approach_ratio == 1:
                    # Projectile hit the bottom-right corner of collided sprite
                    self.direction = self.direction.reflect(Vector2(1, 1))
                elif approach_ratio > 1:
                    # Projectile hit the bottom of collided sprite
                    self.direction = self.direction.reflect(Vector2(0, -1))

            # point_size = (1, 1)
            # projectile_points = {'topleft': (self.rect.topleft, point_size),
            #                      "midtop": (self.rect.midtop, point_size),
            #                      "topright": (self.rect.topright, point_size),
            #                      "midright": (self.rect.midright, point_size),
            #                      "bottomright": (self.rect.bottomright, point_size),
            #                      "midbottom": (self.rect.midbottom, point_size),
            #                      "bottomleft": (self.rect.bottomleft, point_size),
            #                      "midleft": (self.rect.midleft, point_size)}
            # collided_points = collided_sprite.rect.collidedictall(projectile_points, True)
            #
            # for point in collided_points:
            #     if projectile_points["bottomleft"] in point and projectile_points["bottomright"] in point:
            #         # Projectile hit top of collided sprite
            #         self.direction = self.direction.reflect(Vector2(0, -1))
            #         return
            #     elif projectile_points["topleft"] in point and projectile_points["bottomleft"] in point:
            #         # Projectile hit right of collided sprite
            #         self.direction = self.direction.reflect(Vector2(1, 0))
            #         return
            #     elif projectile_points["topleft"] in point and projectile_points["topright"] in point:
            #         # Projectile hit bottom of collided sprite
            #         self.direction = self.direction.reflect(Vector2(0, 1))
            #         return
            #     elif projectile_points["topright"] in point and projectile_points["bottomright"] in point:
            #         # Projectile hit left of collided sprite
            #         self.direction = self.direction.reflect(Vector2(-1, 0))
            #         return
            # TODO: Destroy block

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
        self.launch_angle = 45 # TODO: Set to 90
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
