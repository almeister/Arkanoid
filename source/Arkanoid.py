import os
import sys
import pygame

from settings import Settings
from blocks import Blocks
from spritesheet import SpriteSheet


class Arkanoid:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Arkanoid")
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.clock = pygame.time.Clock()
        self.sprite_sheet = SpriteSheet(os.path.join(self.settings.images_path, "sh_2.png"))
        self.blocks = Blocks(self.screen, self.sprite_sheet)
        self.blocks.place_blocks()

    def run(self):
        while True:
            self.check_events()
            self.update()

            self.clock.tick(30)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()

    def update(self):
        self.screen.fill(self.settings.bg_color)
        self.blocks.update()

        pygame.display.flip()


if __name__ == '__main__':
    arkanoid = Arkanoid()
    arkanoid.run()

