import pygame

from block import BlockType
from blocks import Blocks
from boundaries import Boundaries
from collisiondetector import CollisionDetector
from eventbus import EventBus
from gameevent import BlockHitEvent, GameEvent
from level import Level
from levelloader import LevelLoader
from playercontroller import PlayerController
from powerup import PowerUp
from settings import Settings
from spritegroup import SpriteGroup, SpriteGroupType
from spritesheet import SpriteSheet


class Arkanoid:

    def __init__(self):
        self.settings = Settings()
        self.setup_pygame()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.clock = pygame.time.Clock()
        self.sprite_sheet = SpriteSheet(self.settings.sprites_path, "sh_2.json")
        self.collision_detector = CollisionDetector()
        self.player_controller = PlayerController(lambda: self.level.platform.launch())  # TODO: Use event bus
        self.blocks = Blocks(self.screen, self.sprite_sheet)
        self.event_bus = EventBus()
        self.event_bus.subscribe(BlockHitEvent.TYPE, self, lambda event: self.on_block_hit(event))
        self.boundaries = Boundaries(self.screen.get_rect())
        self.setup_boundaries()
        self.power_up_group = SpriteGroup(SpriteGroupType.POWER_UP)
        self.level = Level(self.screen, self.sprite_sheet, self.event_bus, self.collision_detector, self.player_controller)
        self.load_level()

    def on_block_hit(self, event: GameEvent):
        if event.TYPE == BlockHitEvent.TYPE:
            if event.block.block_type == BlockType.RED:
                sprite_name = "PowerUpRed.png"
                self.drop_power_up(sprite_name, event.position)

            self.blocks.remove_block(event.block)

    def drop_power_up(self, name, position):
        power_up = PowerUp(self.screen, self.sprite_sheet, name, position)
        self.power_up_group.add(power_up)

    def setup_pygame(self):
        pygame.init()
        pygame.display.set_caption("Arkanoid")

    def setup_boundaries(self):
        self.collision_detector.add_sprite_group(self.boundaries.boundary_sprite_group)
        self.collision_detector.add_sprite_group(self.boundaries.out_of_bounds_sprite_group)

    def load_level(self):
        self.collision_detector.add_listener(self.level)
        self.collision_detector.add_sprite_group(self.level.projectile_group)

        level_loader = LevelLoader(self.settings.levels_path)
        level_data = level_loader.load_level("red_block_powerup")
        self.blocks.place_blocks(level_data.get_grid()["origin"], level_data.get_block_size(), level_data.get_blocks())
        self.collision_detector.add_sprite_group(self.blocks.sprite_group)

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

        self.collision_detector.update()
        self.blocks.update()
        self.power_up_group.update(delta_t)

        pygame.display.flip()


if __name__ == '__main__':
    arkanoid = Arkanoid()
    arkanoid.run()
