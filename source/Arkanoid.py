import sys
import pygame

from settings import Settings


class Arkanoid:

    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Arkanoid")

    def run(self):
        while True:
            self.check_events()
            self.update_screen()

            self.clock.tick(30)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()

    def update_screen(self):
        self.screen.fill(self.settings.bg_color)
        pygame.display.flip()


if __name__ == '__main__':
    arkanoid = Arkanoid()
    arkanoid.run()

