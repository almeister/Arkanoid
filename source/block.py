import pygame


class Block:
    block_types = {'yellow': (5, 70), 'red': (83, 70), 'green': (165, 70), 'blue': (243, 70), 'orange': (243, 277)}

    def __init__(self, screen, sprite_sheet, block_type, position, size):
        self.screen = screen
        rect = pygame.Rect(self.block_types[block_type], size)  # TODO: identify block type for pos
        self.image = sprite_sheet.image_at(rect)
        self.position = position

    def move(self, position):
        self.position = position

    def update(self):
        block_rectangle = self.image.get_rect()
        block_rectangle.center = self.position
        self.screen.blit(self.image, block_rectangle)
