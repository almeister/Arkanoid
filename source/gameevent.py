from abc import ABC

from block import Block


class GameEvent(ABC):
    TYPE = "GameEvent: Base event type."


class BlockHitEvent(GameEvent):
    TYPE = "BlockHitEvent: Block hit."

    def __init__(self, block: Block, position):
        GameEvent.__init__(self)
        self.block = block
        self.position = position


class LaunchProjectileEvent(GameEvent):
    TYPE = "LaunchProjectileEvent: Launch projectile."

    def __init__(self, position, angle):
        GameEvent.__init__(self)
        self.position = position
        self.angle = angle
