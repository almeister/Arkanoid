from pygame.sprite import Sprite


class PowerUp(Sprite):
    DROP_SPEED = 400

    def __init__(self, screen, sprite_sheet, name, position):
        Sprite.__init__(self)
        self.screen = screen
        self.image = sprite_sheet.image_by_name(name)
        self.rect = self.image.get_rect()
        self.radius = self.rect.w / 2
        self.rect.center = position

    def update(self, delta_t):
        self.rect.centery += self.DROP_SPEED * delta_t / 1000
        self.screen.blit(self.image, self.rect)

