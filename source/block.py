from enum import Enum

from pygame.sprite import Sprite


class BlockType(Enum):
    ORANGE = 0
    RED = 1
    GREEN = 2
    BLUE = 3


class Block(Sprite):
    BLOCK_TYPES = {
        "OrangeBlock.png": BlockType.ORANGE,
        "RedBlock.png": BlockType.RED,
        "GreenBlock.png": BlockType.GREEN,
        "BlueBlock.png": BlockType.BLUE
    }

    def __init__(self, screen, sprite_sheet, sprite_name, position):
        Sprite.__init__(self)
        self.screen = screen
        self.image = sprite_sheet.image_by_name(sprite_name)
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.block_type = self.BLOCK_TYPES[sprite_name] if sprite_name in self.BLOCK_TYPES else None

    def update(self):
        self.screen.blit(self.image, self.rect)
