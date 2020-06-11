import pygame

from block import Block
from cartesiantypes import Point


class Blocks:
    block_sprites = {'yellow': 'YellowBlock.png', 'red': 'RedBlock.png', 'green': 'GreenBlock.png',
                     'blue': 'BlueBlock.png',
                     'orange': 'OrangeBlock.png'}

    def __init__(self, screen, sprite_sheet):
        self.screen = screen
        self.sprite_sheet = sprite_sheet
        self.blocks = []
        self.sprite_group = pygame.sprite.Group()

    def place_blocks(self, origin, block_size, blocks):
        for block in blocks:
            block_pos = Point(origin["x"] + block['grid_position']['x'] * block_size["w"],
                              origin["y"] + block['grid_position']['y'] * block_size["h"])
            self.place_block(block["type"], block_pos)

    def place_block(self, block_type, position):
        block = Block(self.screen, self.sprite_sheet, self.block_sprites[block_type], position)
        self.blocks.append(block)
        self.sprite_group.add(block)

    def update(self):
        for block in self.blocks:
            block.update()
