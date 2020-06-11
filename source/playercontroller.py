import pygame
import sys

from enum import Enum


class Movement(Enum):
    IDLE = 0
    LEFT = 1
    RIGHT = 2


class PlayerController:

    def __init__(self, on_fire):
        self.movement = Movement.IDLE
        self.on_fire = on_fire

    def poll_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()
                elif event.key == pygame.K_LEFT:
                    self.movement = Movement.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.movement = Movement.RIGHT

                if event.key == pygame.K_SPACE:
                    self.on_fire()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.movement = Movement.IDLE

    def update(self):
        self.poll_events()
