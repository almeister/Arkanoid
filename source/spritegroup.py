import pygame

from enum import Enum


class SpriteGroupType(Enum):
    SPACE_BALL = 0,
    BLOCKS = 1


class SpriteGroup(pygame.sprite.Group):

    def __init__(self, group_type):
        pygame.sprite.Group.__init__(self)
        self.group_type = group_type
