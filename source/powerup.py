from pygame.sprite import Sprite


class PowerUp(Sprite):
    DROP_SPEED = 10

    def __init__(self, screen, sprite_sheet, name, position):
        Sprite.__init__(self)
        self.screen = screen
        self.sprite_sheet = sprite_sheet
        self.image = sprite_sheet.image_by_name(name)
        self.rect = self.image.get_rect()
        self.rect.center = position

    def update(self, delta_t):
        # Move with gravity
        self.rect.centery += self.DROP_SPEED * delta_t
        # Check for collisions with platform
        self.screen.blit(self.image, self.rect)