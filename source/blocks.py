from block import Block


class Blocks:

    def __init__(self, screen, sprite_sheet):
        self.screen = screen
        self.sprite_sheet = sprite_sheet
        self.blocks = []
        self.size = (67, 27)

    def place_block(self, position):
        block = Block(self.screen, self.sprite_sheet, position, self.size)
        self.blocks.append(block)

    def update(self):
        for block in self.blocks:
            block.update()

