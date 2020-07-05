from eventsubscriber import EventSubscriber
from gameevent import LaunchProjectileEvent
from observer import Observer
from playerplatform import PlayerPlatform
from projectile import Projectile
from spritegroup import SpriteGroup, SpriteGroupType


class Level(EventSubscriber, Observer):

    def __init__(self, screen, sprite_sheet, event_bus, collision_detector, player_controller):
        EventSubscriber.__init__(self, event_bus)
        self.screen = screen
        self.sprite_sheet = sprite_sheet
        self.collision_detector = collision_detector
        self.player_controller = player_controller
        self.platform = PlayerPlatform(self.screen, self.sprite_sheet, self.collision_detector, self.event_bus)
        self.setup_player_platform()
        self.projectile_group = SpriteGroup(SpriteGroupType.SPACE_BALL)
        self.subscribe_to_events()

    def subscribe_to_events(self):
        self.subscribe(LaunchProjectileEvent.TYPE, lambda event: self.on_launch_projectile(event))

    def on_observed(self, collision_detector) -> None:
        sprite_group = collision_detector.collided_sprite_group
        if sprite_group.group_type == SpriteGroupType.OUT_OF_BOUNDS:
            self.platform.reset_projectile()
            self.projectile_group.remove(collision_detector.colliding_sprite)

    def setup_player_platform(self):
        self.collision_detector.add_sprite_group(self.platform.sprite_group)

    def on_launch_projectile(self, event):
        if event.TYPE == LaunchProjectileEvent.TYPE:
            self.launch_projectile(event.position, event.angle)

    def launch_projectile(self, position, angle):
        projectile = Projectile(self.screen, self.sprite_sheet, Projectile.types["small"], self.collision_detector, self.event_bus)
        projectile.rect.center = position
        projectile.launch(angle)
        self.projectile_group.add(projectile)

    def update(self, delta_t):
        self.platform.move(self.player_controller.movement, delta_t)
        self.platform.update(delta_t)
        self.projectile_group.update(delta_t)
