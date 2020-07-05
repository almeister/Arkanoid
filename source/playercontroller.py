import pygame
import sys

from enum import Enum


class Movement(Enum):
    IDLE = 0
    LEFT = 1
    RIGHT = 2


class PlayerController:

    def __init__(self, on_space_key):
        self.movement = Movement.IDLE
        self.on_space_key = on_space_key
        self.movement_keys_down = []

    def poll_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()
                elif event.key == pygame.K_LEFT:
                    self.movement = Movement.LEFT
                    self.movement_keys_down.append(event.key)
                elif event.key == pygame.K_RIGHT:
                    self.movement = Movement.RIGHT
                    self.movement_keys_down.append(event.key)

                if event.key == pygame.K_SPACE:
                    self.on_space_key()
            elif event.type == pygame.KEYUP:
                if (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT) and len(self.movement_keys_down) == 1:
                    self.movement = Movement.IDLE

                if event.key in self.movement_keys_down:
                    self.movement_keys_down.remove(event.key)

    def update(self):
        self.poll_events()
