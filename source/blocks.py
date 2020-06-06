from collections import namedtuple
from block import Block


class Blocks:
    Position = namedtuple('Position', ['x', 'y'])
    Size = namedtuple('Size', ['width', 'height'])

    def __init__(self, screen, sprite_sheet):
        self.screen = screen
        self.sprite_sheet = sprite_sheet
        self.blocks = []
        self.size = self.Size(67, 27)
        self.spacing = self.Size(5, 0)

    def place_blocks(self):
        block_pos = self.Position(self.screen.get_rect().center[0], self.screen.get_rect().center[1])
        for block_type in Block.block_types:
            self.place_block(block_type, block_pos)
            block_pos = self.Position(block_pos.x + self.size.width + self.spacing.width, block_pos.y)

    def place_block(self, block_type, position):
        block = Block(self.screen, self.sprite_sheet, block_type, position, self.size)
        self.blocks.append(block)

    def update(self):
        for block in self.blocks:
            block.update()

