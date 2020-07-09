import os

import pygame

from eventbus import EventBus
from level import Level
from playercontroller import PlayerController
from settings import Settings
from spritesheet import SpriteSheet


class Arkanoid:

    def __init__(self):
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.event_bus = EventBus()
        self.clock = pygame.time.Clock()
        self.sprite_sheet = SpriteSheet(self.settings.sprites_path, "sh_2.json")
        self.player_controller = PlayerController(lambda: self.level.platform.launch())  # TODO: Use event bus
        self.level = Level(self.screen, self.sprite_sheet, self.event_bus, self.player_controller)

        self.init()

    def init(self):
        pygame.init()
        pygame.display.set_caption("Arkanoid")

        self.level.load_from_file(os.path.join(self.settings.levels_path, "level_red_block_powerup.json"))

    def run(self):
        delta_t = 0
        while True:
            self.update(delta_t)
            delta_t = self.clock.tick(60)

    def update(self, delta_t):
        self.event_bus.update()

        self.screen.fill(self.settings.bg_color)

        self.player_controller.update()
        self.level.update(delta_t)

        pygame.display.flip()


if __name__ == '__main__':
    arkanoid = Arkanoid()
    arkanoid.run()
