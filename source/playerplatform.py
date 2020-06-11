import operator
import pygame

from projectile import Projectile
from playercontroller import Movement


class PlayerPlatform(pygame.sprite.Sprite):
    platform_sprites = {'small': 'SmallPlatform.png', 'medium': 'MediumPlatform.png', 'large': 'LargePlatform.png'}
    BOTTOM_SPACING = 80
    MOVEMENT_SPEED = 900

    def __init__(self, screen, sprite_sheet):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.sprite_sheet = sprite_sheet
        self.image = self.sprite_sheet.image_by_name(self.platform_sprites['small'])
        self.rect = self.image.get_rect()
        self.rect.center = (screen.get_rect().midbottom[0], screen.get_rect().midbottom[1] -
                            self.BOTTOM_SPACING)
        self.projectile = Projectile(self.screen, self.sprite_sheet, Projectile.types["small"])
        self.projectile_sprite_group = pygame.sprite.Group()
        self.projectile_sprite_group.add(self.projectile)

    def move(self, movement, delta_t):
        distance = self.MOVEMENT_SPEED * delta_t / 1000
        if movement == Movement.LEFT:
            distance = -distance
        elif movement == Movement.RIGHT:
            pass
        else:
            distance = 0

        self.rect.center = tuple(map(operator.add, self.rect.center, (distance, 0)))

        if not self.projectile.is_in_flight():
            projectile_position = (self.rect.centerx, self.rect.centery - self.projectile.rect.w)
            self.projectile.update_launch_angle(movement)
            self.projectile.set_position(projectile_position)

    def fire(self):
        self.projectile.fire()

    def update(self, delta_t, blocks_group):
        self.screen.blit(self.image, self.rect)
        self.projectile.update(delta_t, blocks_group)
