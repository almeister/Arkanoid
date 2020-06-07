

class Block:

    def __init__(self, screen, sprite_sheet, sprite_name, position):
        self.screen = screen
        self.image = sprite_sheet.image_by_name(sprite_name)
        self.position = position

    def update(self):
        block_rectangle = self.image.get_rect()
        block_rectangle.center = self.position
        self.screen.blit(self.image, block_rectangle)
