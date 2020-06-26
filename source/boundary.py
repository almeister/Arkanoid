from pygame.sprite import Sprite


class Boundary(Sprite):

    def __init__(self, rect):
        Sprite.__init__(self)
        self.rect = rect
