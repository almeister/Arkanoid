from abc import ABC

from block import BlockType


class GameEvent(ABC):
    TYPE = "GameEvent: Base event type."


class BlockHitEvent(GameEvent):
    TYPE = "BlockHitEvent: Block hit."

    def __init__(self, block_type: BlockType, position):
        GameEvent.__init__(self)
        self.block_type = block_type
        self.position = position

