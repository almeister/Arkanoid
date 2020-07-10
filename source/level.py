from block import BlockType
from blocks import Blocks
from boundaries import Boundaries
from collisiondetector import CollisionDetector
from eventsubscriber import EventSubscriber
from gameevent import LaunchProjectileEvent, BlockHitEvent, GameEvent
from levelloader import LevelLoader
from icollisiondetector import ICollisionDetectorListener
from playerplatform import PlayerPlatform
from powerup import PowerUp
from projectile import Projectile
from spritegroup import SpriteGroup, SpriteGroupType


class Level(EventSubscriber, ICollisionDetectorListener):

    def __init__(self, screen, sprite_sheet, event_bus, player_controller):
        EventSubscriber.__init__(self, event_bus)
        self.screen = screen
        self.sprite_sheet = sprite_sheet
        self.player_controller = player_controller
        self.collision_detector = CollisionDetector()
        self.boundaries = Boundaries(self.screen.get_rect())
        self.blocks = Blocks(self.screen, self.sprite_sheet)
        self.platform = PlayerPlatform(self.screen, self.sprite_sheet, self.collision_detector, self.event_bus)
        self.projectile_group = SpriteGroup(SpriteGroupType.SPACE_BALLS)
        self.power_up_group = SpriteGroup(SpriteGroupType.POWER_UPS)

        self.init()

    def init(self):
        self.setup_collision_detection()
        self.setup_player_platform()

        self.subscribe_to_events()

    def load_from_file(self, file_path):
        level_loader = LevelLoader()
        level_data = level_loader.load_level(file_path)

        self.blocks.place_blocks(level_data.get_grid()["origin"], level_data.get_block_size(), level_data.get_blocks())
        self.collision_detector.add_sprite_group(self.blocks.sprite_group)

    def subscribe_to_events(self):
        self.subscribe(LaunchProjectileEvent.TYPE, lambda event: self.on_launch_projectile(event))
        self.subscribe(BlockHitEvent.TYPE, lambda event: self.on_block_hit(event))

    def setup_collision_detection(self):
        self.collision_detector.add_listener(self)
        self.collision_detector.add_sprite_group(self.projectile_group)
        self.collision_detector.add_sprite_group(self.power_up_group)
        self.collision_detector.add_sprite_group(self.boundaries.boundary_sprite_group)
        self.collision_detector.add_sprite_group(self.boundaries.out_of_bounds_sprite_group)

    def setup_player_platform(self):
        self.collision_detector.add_sprite_group(self.platform.sprite_group)

    def on_collision(self, collision_detector) -> None:
        collided_sprite_group = collision_detector.collided_sprite_group
        colliding_sprite_group = collision_detector.colliding_sprite_group
        if colliding_sprite_group.group_type == SpriteGroupType.SPACE_BALLS and collided_sprite_group.group_type == SpriteGroupType.OUT_OF_BOUNDS:
            self.platform.reset_projectile()
            self.platform.disarm_turrets()
            self.projectile_group.remove(collision_detector.colliding_sprite)
        elif colliding_sprite_group.group_type == SpriteGroupType.POWER_UPS and collided_sprite_group.group_type == SpriteGroupType.PLATFORM:
            self.platform.arm_turrets()
            self.power_up_group.remove(collision_detector.colliding_sprite)

    def on_block_hit(self, event: GameEvent):
        if event.TYPE == BlockHitEvent.TYPE:
            if event.block.block_type == BlockType.RED:
                sprite_name = "PowerUpRed.png"
                self.drop_power_up(sprite_name, event.position)

            self.blocks.remove_block(event.block)

    def on_launch_projectile(self, event):
        if event.TYPE == LaunchProjectileEvent.TYPE:
            self.launch_projectile(event.position, event.angle)

    def launch_projectile(self, position, angle):
        projectile = Projectile(self.screen, self.sprite_sheet, Projectile.types["small"], self.collision_detector,
                                self.event_bus)
        projectile.rect.center = position
        projectile.launch(angle)
        self.projectile_group.add(projectile)

    def drop_power_up(self, name, position):
        power_up = PowerUp(self.screen, self.sprite_sheet, name, position)
        self.power_up_group.add(power_up)

    def update(self, delta_t):
        self.collision_detector.update()

        self.platform.move(self.player_controller.movement, delta_t)
        self.platform.update(delta_t)
        self.projectile_group.update(delta_t)
        self.blocks.update()
        self.power_up_group.update(delta_t)
