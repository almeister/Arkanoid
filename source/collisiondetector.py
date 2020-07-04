import pygame
from pygame.math import Vector2

from observer import Observer, Observable


class CollisionDetector(Observable):

    def __init__(self):
        self.listeners = []
        self.sprites = []
        self.sprite_groups = []
        self.collided_sprite_group = None
        self.collided_sprites = []

    def add_listener(self, observer: Observer) -> None:
        self.listeners.append(observer)

    def remove_listener(self, observer: Observer) -> None:
        self.listeners.remove(observer)

    def notify(self) -> None:
        [listener.on_observed(self) for listener in self.listeners]

    def add_sprite(self, sprite):
        self.sprites.append(sprite)

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

    def update(self):
        self.collided_sprite_group = None
        self.collided_sprites = []
        for sprite in self.sprites:
            for sprite_group in self.sprite_groups:
                self.collided_sprite_group = sprite_group  # TODO: send sprite_group and collided_sprite in event
                self.collided_sprites = pygame.sprite.spritecollide(sprite, sprite_group, False,
                                                                    self.collided_with_circle)
                if self.collided_sprites:
                    self.notify()
