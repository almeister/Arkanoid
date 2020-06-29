from pygame.sprite import Sprite


class Turrets(Sprite):

    def __init__(self, screen, sprite_sheet, sprite_name):
        Sprite.__init__(self)
        self.screen = screen
        self.sprite_sheet = sprite_sheet
        self.image = self.sprite_sheet.image_by_name(sprite_name)
        self.rect = self.image.get_rect()
        self.y_offset = 7

    def set_position(self, position):
        self.rect.center = position

    def update(self):
        self.screen.blit(self.image, self.rect)

