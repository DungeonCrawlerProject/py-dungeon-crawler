import time

import pygame

from Scripts.Player.PlayerStateMachine.player_state import PlayerState


class PlayerIdle(PlayerState):


    def __init__(self):
        super().__init__(None)


    def do_state(player):
        """
        Determines if player state needs to change states and calls Idle method
        :param player: Instance of player class
        :returns: Returns IPlayerState interface
        """

        # Get the state of all keys
        keys = pygame.key.get_pressed()

        # Update player position based on key input
        if any([keys[pygame.K_w], keys[pygame.K_s], keys[pygame.K_a], keys[pygame.K_d]]):
            return player.playerMove

        if keys[pygame.K_SPACE] and player.next_dodge < time.time():
            return player.player_dodge

        return player.playerIdle

    def idle(self):
        # ToDo: Play animation that corresponds to look direction
        raise NotImplementedError
