import pygame
from pygame.math import Vector2

from icollisiondetector import ICollisionDetectorListener, ICollisionDetector
from spritegroup import SpriteGroupType


class CollisionDetector(ICollisionDetector):

    def __init__(self):
        self.listeners = []
        self.sprite_groups = []
        self.colliding_sprite = None
        self.colliding_sprite_group = None
        self.collided_sprite_group = None
        self.collided_sprites = []

    def add_listener(self, observer: ICollisionDetectorListener) -> None:
        self.listeners.append(observer)

    def remove_listener(self, observer: ICollisionDetectorListener) -> None:
        self.listeners.remove(observer)

    def notify(self) -> None:
        [listener.on_collision(self) for listener in self.listeners]

    def add_sprite_group(self, sprite_group):
        self.sprite_groups.append(sprite_group)

    def clamp(self, minimum, maximum, value):
        return max(minimum, min(maximum, value))

    def collided_with_circle(self, sprite_circle, sprite_rect):
        point_on_block = Vector2(self.clamp(sprite_rect.rect.x,
                                            sprite_rect.rect.x + sprite_rect.rect.w,
                                            sprite_circle.rect.center[0]),
                                 self.clamp(sprite_rect.rect.y,
                                            sprite_rect.rect.y + sprite_rect.rect.h,
                                            sprite_circle.rect.center[1]))
        circle_centre_to_block = sprite_circle.rect.center - point_on_block

        return circle_centre_to_block.magnitude() < sprite_circle.radius

    def find_group(self, group_type):
        for sprite_group in self.sprite_groups:
            if sprite_group.group_type == group_type:
                return sprite_group

        return None

    def notify_collisions_for_group(self, group_type):
        self.colliding_sprite = None
        self.colliding_sprite_group = None
        self.collided_sprite_group = None
        self.collided_sprites = []
        group = self.find_group(group_type)

        if group:
            for sprite in group.sprites():
                for sprite_group in self.sprite_groups:
                    if sprite_group.group_type != group_type:
                        self.collided_sprites = pygame.sprite.spritecollide(sprite, sprite_group, False,
                                                                            self.collided_with_circle)
                        if self.collided_sprites:
                            self.colliding_sprite = sprite
                            self.colliding_sprite_group = group
                            self.collided_sprite_group = sprite_group
                            self.notify()

    def update(self):
        self.notify_collisions_for_group(SpriteGroupType.SPACE_BALLS)
        self.notify_collisions_for_group(SpriteGroupType.POWER_UPS)
