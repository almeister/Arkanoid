import operator
from pygame.sprite import Sprite

from gameevent import LaunchProjectileEvent
from projectile import Projectile
from playercontroller import Movement
from spritegroup import SpriteGroup, SpriteGroupType
from turrets import Turrets


class PlayerPlatform(Sprite):
    platform_sprites = {'small': 'SmallPlatform.png', 'medium': 'MediumPlatform.png', 'large': 'LargePlatform.png'}
    BOTTOM_SPACING = 80
    MOVEMENT_SPEED = 700
    LAUNCH_ANGLE_INCREMENT = 3
    REST_LAUNCH_ANGLE = 90

    def __init__(self, screen, sprite_sheet, collision_detector, event_bus):
        Sprite.__init__(self)
        self.sprite_group = SpriteGroup(SpriteGroupType.PLATFORM)  # TODO: Move to Level
        self.screen = screen
        self.sprite_sheet = sprite_sheet
        self.event_bus = event_bus
        self.image = self.sprite_sheet.image_by_name(self.platform_sprites['small'])
        self.rect = self.image.get_rect()
        self.rect.center = (screen.get_rect().midbottom[0], screen.get_rect().midbottom[1] -
                            self.BOTTOM_SPACING)
        self.sprite_group.add(self)
        self.movement = Movement.IDLE
        self.launch_angle = self.REST_LAUNCH_ANGLE
        self.projectile = Projectile(self.screen, self.sprite_sheet, Projectile.types["small"], collision_detector,
                                     event_bus)
        self.turrets = None

    def move(self, movement, delta_t):
        distance = self.MOVEMENT_SPEED * delta_t / 1000
        if movement == Movement.LEFT:
            distance = -distance
        elif movement == Movement.RIGHT:
            pass
        else:
            distance = 0

        self.rect.center = tuple(map(operator.add, self.rect.center, (distance, 0)))

        if self.projectile:
            projectile_position = (self.rect.centerx, self.rect.centery - self.projectile.rect.w)
            self.projectile.set_position(projectile_position)
            self.update_launch_angle(movement)

        if self.turrets:
            self.turrets.set_position((self.rect.centerx, self.rect.top + self.turrets.y_offset))

    def update_launch_angle(self, movement):
        if self.movement == movement:
            if movement == Movement.LEFT:
                self.launch_angle = max(30, self.launch_angle - self.LAUNCH_ANGLE_INCREMENT)
            elif movement == Movement.RIGHT:
                self.launch_angle = min(150, self.launch_angle + self.LAUNCH_ANGLE_INCREMENT)
            else:
                self.reset_movement()
        else:
            self.reset_movement()

        self.movement = movement

    def reset_movement(self):
        self.movement = Movement.IDLE
        self.launch_angle = self.REST_LAUNCH_ANGLE

    def reset_projectile(self):
        self.projectile.show()

    def launch(self):
        launch_event = LaunchProjectileEvent(self.projectile.rect.center, self.launch_angle)
        self.event_bus.publish(launch_event)
        self.projectile.hide()

    def arm_turrets(self):
        self.turrets = Turrets(self.screen, self.sprite_sheet, "SmallTurrets.png")

    def disarm_turrets(self):
        self.turrets = None

    def update(self, delta_t):
        self.screen.blit(self.image, self.rect)
        self.projectile.update(delta_t)
        if self.turrets:
            self.turrets.update()
