from pygame.sprite import Sprite


class Block(Sprite):

    def __init__(self, screen, sprite_sheet, sprite_name, position):
        Sprite.__init__(self)
        self.screen = screen
        self.image = sprite_sheet.image_by_name(sprite_name)
        self.rect = self.image.get_rect()
        self.rect.center = position

    def update(self):
        self.screen.blit(self.image, self.rect)
