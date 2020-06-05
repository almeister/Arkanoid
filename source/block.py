import pygame


class Block:

    def __init__(self, screen, sprite_sheet, position, size):
        self.screen = screen
        rect = pygame.Rect((5, 70), size)  # TODO: identify block type for pos
        self.image = sprite_sheet.image_at(rect)
        self.position = position

    def move(self, position):
        self.position = position

    def update(self):
        block_rectangle = self.image.get_rect()
        block_rectangle.topleft = self.position
        self.screen.blit(self.image, block_rectangle)
