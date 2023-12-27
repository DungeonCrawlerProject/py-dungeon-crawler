import time

import pygame

from Scripts.Player.PlayerStateMachine.player_state import PlayerState


class PlayerMove(PlayerState):

    def __init__(self):
        super().__init__(None)

    def do_state(self, player):
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

    def move(self, player):
        """
        Gets direction that player needs to move from keyboard inputs
        :param player: Instance of player class
        """
        # Update player position based on key input
        # if keys[pygame.K_w]:
        #     movement_input.y = -1
        # if keys[pygame.K_s]:
        #     movement_input.y = 1
        # if keys[pygame.K_a]:
        #     movement_input.x = -1
        # if keys[pygame.K_d]:
        #     movement_input.x = 1
        #
        # player.moveDirection.x = Input.GetAxisRaw("Horizontal");
        # player.moveDirection.y = Input.GetAxisRaw("Vertical");
        #
        # player.moveDirection.Normalize();
        ...
