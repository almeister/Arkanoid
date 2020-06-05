import sys
import pygame
import os

from settings import Settings
from spritesheet import SpriteSheet


class Arkanoid:

    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Arkanoid")
        self.spritesheet = SpriteSheet(os.path.join(self.settings.images_path, "sh_2.png"))

    def run(self):
        while True:
            self.check_events()
            self.update_screen()

            self.clock.tick(30)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()

    def update_screen(self):
        self.screen.fill(self.settings.bg_color)
        block = self.spritesheet.image_at((5, 70, 67, 27))

        block_rectangle = block.get_rect()
        block_rectangle.topleft = pygame.display.get_surface().get_rect().center
        self.screen.blit(block, block_rectangle)

        pygame.display.flip()


if __name__ == '__main__':
    arkanoid = Arkanoid()
    arkanoid.run()

