import pygame

from enum import Enum


class SpriteGroupType(Enum):
    SPACE_BALLS = 0,
    BLOCKS = 1,
    BOUNDARIES = 2,
    OUT_OF_BOUNDS = 3,
    PLATFORM = 4,
    POWER_UPS = 5


class SpriteGroup(pygame.sprite.Group):

    def __init__(self, group_type):
        pygame.sprite.Group.__init__(self)
        self.group_type = group_type

