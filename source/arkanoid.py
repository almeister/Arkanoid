import pygame

from blocks import Blocks
from playercontroller import PlayerController
from playerplatform import PlayerPlatform
from settings import Settings
from spritesheet import SpriteSheet


class Arkanoid:

    def __init__(self):
        self.setup_pygame()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.clock = pygame.time.Clock()
        self.sprite_sheet = SpriteSheet(self.settings.images_path, "sh_2.json")
        self.blocks = Blocks(self.screen, self.sprite_sheet)
        self.platform = PlayerPlatform(self.screen, self.sprite_sheet)
        self.player_controller = PlayerController()
        self.load_level()

    def setup_pygame(self):
        pygame.init()
        pygame.display.set_caption("Arkanoid")

    def load_level(self):
        self.blocks.place_blocks()

    def run(self):
        while True:
            self.player_controller.update()
            self.update()

            self.clock.tick(60)

    def update_movement(self):
        self.platform.move(self.player_controller.get_movement())

    def update(self):
        self.screen.fill(self.settings.bg_color)
        self.update_movement()
        self.platform.update()
        self.blocks.update()

        pygame.display.flip()


if __name__ == '__main__':
    arkanoid = Arkanoid()
    arkanoid.run()
