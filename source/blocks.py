from collections import namedtuple
from block import Block


class Blocks:
    block_types = {'yellow': 'YellowBlock.png', 'red': 'RedBlock.png', 'green': 'GreenBlock.png',
                   'blue': 'BlueBlock.png',
                   'orange': 'OrangeBlock.png'}
    Position = namedtuple('Position', ['x', 'y'])  # TODO: Remove these typedefs
    Size = namedtuple('Size', ['width', 'height'])

    def __init__(self, screen, sprite_sheet):
        self.screen = screen
        self.sprite_sheet = sprite_sheet
        self.blocks = []
        self.block_size = self.Size(67, 27)
        self.spacing = self.Size(5, 0)

    # TODO: Replace with LevelLoader.load_level(name)
    def place_blocks(self):
        block_pos = self.Position(self.screen.get_rect().centerx, self.screen.get_rect().centery)
        for block_type in self.block_types:
            self.place_block(block_type, block_pos)
            block_pos = self.Position(block_pos.x + self.block_size.width + self.spacing.width, block_pos.y)

    def place_block(self, block_type, position):
        block = Block(self.screen, self.sprite_sheet, self.block_types[block_type], position)
        self.blocks.append(block)

    def update(self):
        for block in self.blocks:
            block.update()
