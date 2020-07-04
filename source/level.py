from eventbus import EventBus
from gameevent import BlockHitEvent, GameEvent
from powerup import PowerUp
from spritegroup import SpriteGroup, SpriteGroupType


class Level:

    def __init__(self, screen, sprite_sheet):
        self.screen = screen
        self.sprite_sheet = sprite_sheet

    def update(self, delta_t):
        pass
