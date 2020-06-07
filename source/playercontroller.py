import pygame
import sys

from enum import Enum


class Movement(Enum):
    IDLE = 0
    LEFT = 1
    RIGHT = 2


class PlayerController:
    movement_speed = 15

    def __init__(self):
        self.movement = Movement.IDLE

    def poll_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # TODO: Fix bug when left and right both pressed
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()
                elif event.key == pygame.K_LEFT:
                    self.movement = Movement.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.movement = Movement.RIGHT
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.movement = Movement.IDLE

    def get_movement(self):
        if self.movement == Movement.LEFT:
            return -self.movement_speed
        elif self.movement == Movement.RIGHT:
            return self.movement_speed
        else:
            return 0

    def update(self):
        self.poll_events()
