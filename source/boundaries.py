from pygame.rect import Rect

from boundary import Boundary
from spritegroup import SpriteGroup, SpriteGroupType


class Boundaries:
    BOUNDARY_BREADTH = 100

    def __init__(self, screen_rect):
        self.screen_rect = screen_rect
        self.boundaries = []
        self.boundary_sprite_group = SpriteGroup(SpriteGroupType.BOUNDARIES)
        self.place_boundaries()

    def place_boundaries(self):
        self.place_boundary(Rect((0, -self.BOUNDARY_BREADTH), (self.screen_rect.w, self.BOUNDARY_BREADTH)))  # top
        self.place_boundary(Rect((-self.BOUNDARY_BREADTH, 0), (self.BOUNDARY_BREADTH, self.screen_rect.h)))  # left
        self.place_boundary(Rect((self.screen_rect.w, 0), (self.BOUNDARY_BREADTH, self.screen_rect.h)))  # right

    def place_boundary(self, rect):
        boundary = Boundary(rect)
        self.boundaries.append(boundary)
        self.boundary_sprite_group.add(boundary)
