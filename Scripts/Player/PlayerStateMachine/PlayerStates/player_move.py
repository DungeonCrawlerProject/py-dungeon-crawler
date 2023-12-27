import math
import time
from dataclasses import dataclass

import pygame

from Scripts.Player.PlayerStateMachine.player_state import IPlayerState


# TODO Position is temp
@dataclass
class Position:
    x: float
    y: float


class PlayerMove(IPlayerState):

    def __init__(self):
        super().__init__(None)

    @staticmethod
    def do_state(player):
        """Determines if player state needs to change states and calls Move method
        :param player: Instance of player class
        :returns: Returns PlayerState interface
        """

        # Get the state of all keys
        keys = pygame.key.get_pressed()

        # Update player position based on key input
        if any([keys[pygame.K_w], keys[pygame.K_s], keys[pygame.K_a], keys[pygame.K_d]]):
            return player.playerMove

        if keys[pygame.K_SPACE] and player.next_dodge < time.time():
            return player.player_dodge

        return player.playerIdle

    @staticmethod
    def move(player):
        """
        Gets direction that player needs to move from keyboard inputs
        :param player: Instance of player class
        """

        # Get the state of all keys
        keys = pygame.key.get_pressed()

        # Update player position based on key input
        movement_input = Position(0, 0)

        # Update player position based on key input
        if keys[pygame.K_w]:
            movement_input.y = -1
        if keys[pygame.K_s]:
            movement_input.y = 1
        if keys[pygame.K_a]:
            movement_input.x = -1
        if keys[pygame.K_d]:
            movement_input.x = 1

        mag = math.sqrt(movement_input.x ** 2 + movement_input.y ** 2)
        if keys[pygame.K_LSHIFT]:
            player.position.x += player.stats.speed * movement_input.x * player.stats.sprint_factor / mag
            player.position.y += player.stats.speed * movement_input.y * player.stats.sprint_factor / mag
        elif mag != 0:
            player.position.x += player.stats.speed * movement_input.x / mag
            player.position.y += player.stats.speed * movement_input.y / mag
