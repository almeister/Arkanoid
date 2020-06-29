import pygame

from blocks import Blocks
from boundaries import Boundaries
from collisiondetector import CollisionDetector
from levelloader import LevelLoader
from playercontroller import PlayerController
from playerplatform import PlayerPlatform
from settings import Settings
from spritesheet import SpriteSheet


class Arkanoid:

    def __init__(self):
        self.settings = Settings()
        self.setup_pygame()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.clock = pygame.time.Clock()
        self.sprite_sheet = SpriteSheet(self.settings.sprites_path, "sh_2.json")
        self.collision_detector = CollisionDetector()
        self.blocks = Blocks(self.screen, self.sprite_sheet)
        self.player_controller = PlayerController(lambda: self.platform.launch())
        self.platform = PlayerPlatform(self.screen, self.sprite_sheet, self.collision_detector)
        self.setup_player_platform()
        self.boundaries = Boundaries(self.screen.get_rect())
        self.setup_boundaries()
        self.load_level()

    def setup_pygame(self):
        pygame.init()
        pygame.display.set_caption("Arkanoid")

    def setup_player_platform(self):
        self.collision_detector.add_sprite_group(self.platform.sprite_group)

    def setup_boundaries(self):
        self.collision_detector.add_sprite_group(self.boundaries.boundary_sprite_group)

    def load_level(self):
        level_loader = LevelLoader(self.settings.levels_path)
        level_data = level_loader.load_level(1)
        self.blocks.place_blocks(level_data.get_grid()["origin"], level_data.get_block_size(), level_data.get_blocks())
        self.collision_detector.add_sprite_group(self.blocks.sprite_group)

    def run(self):
        delta_t = 0
        while True:
            self.update(delta_t)
            delta_t = self.clock.tick(60)

    def update(self, delta_t):
        self.screen.fill(self.settings.bg_color)

        self.player_controller.update()

        self.platform.move(self.player_controller.movement, delta_t)

        self.platform.update(delta_t, self.blocks.sprite_group)
        self.collision_detector.update()
        self.blocks.update()

        pygame.display.flip()


if __name__ == '__main__':
    arkanoid = Arkanoid()
    arkanoid.run()
