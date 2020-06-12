import pygame

from observer import Observer, Observable


class CollisionDetector(Observable):

    def __init__(self):
        self.listeners = []
        self.sprites = []
        self.sprite_groups = []
        self.collided_sprite_group_type = None
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

    def update(self):
        self.collided_sprite_group_type = None
        self.collided_sprites = []
        for sprite in self.sprites:
            for sprite_group in self.sprite_groups:
                self.collided_sprite_group_type = sprite_group.group_type
                self.collided_sprites = pygame.sprite.spritecollide(sprite, sprite_group, False)
                if self.collided_sprites:
                    # TODO: handle simultaneous collisions
                    self.notify()
