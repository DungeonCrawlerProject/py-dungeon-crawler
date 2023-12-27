import time

import pygame

from Scripts.Player.PlayerStateMachine.player_state import IPlayerState


class PlayerDodge(IPlayerState):

    def __init__(self):
        super().__init__(None)
        self._dodge_start_time = 10.0
        self._can_dodge = True

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

    def dodge(self, player):
        """
        Moves the player in a fixed direction at a faster speed
        :param player: Instance of player class
        """

        if self._can_dodge:
            # _x = Input.GetAxisRaw("Horizontal")
            # _y = Input.GetAxisRaw("Vertical")
            # player.move(_x, _y)
            self._dodge_start_time = time.time()
            # player.nextDodge = Time.time + player.dodgeDelay;
            self._can_dodge = False

        if player.next_dodge < time.time():
            self._can_dodge = True
