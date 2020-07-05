from pygame.rect import Rect

from boundary import Boundary
from spritegroup import SpriteGroup, SpriteGroupType


class Boundaries:
    BOUNDARY_BREADTH = 100

    def __init__(self, screen_rect):
        self.screen_rect = screen_rect
        self.boundary_sprite_group = SpriteGroup(SpriteGroupType.BOUNDARIES)
        self.out_of_bounds_sprite_group = SpriteGroup(SpriteGroupType.OUT_OF_BOUNDS)
        self.place_boundaries()

    def place_boundaries(self):
        self.place_boundary(self.boundary_sprite_group,
                            Rect((0, -self.BOUNDARY_BREADTH), (self.screen_rect.w, self.BOUNDARY_BREADTH)))  # top
        self.place_boundary(self.boundary_sprite_group,
                            Rect((-self.BOUNDARY_BREADTH, 0), (self.BOUNDARY_BREADTH, self.screen_rect.h)))  # left
        self.place_boundary(self.boundary_sprite_group,
                            Rect((self.screen_rect.w, 0), (self.BOUNDARY_BREADTH, self.screen_rect.h)))  # right
        self.place_boundary(self.out_of_bounds_sprite_group,
                            Rect((0, self.screen_rect.h), (self.screen_rect.w, self.BOUNDARY_BREADTH)))  # bottom

    def place_boundary(self, sprite_group, rect):
        boundary = Boundary(rect)
        sprite_group.add(boundary)
