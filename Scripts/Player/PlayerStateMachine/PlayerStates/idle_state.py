"""
Idle State
By: Sean McClanahan
Last Modified: 01/04/2024
"""

import pygame

from GameData.game_controls import GameControls
from Scripts.Player.PlayerStateMachine.player_state import IPlayerState


class IdleState(IPlayerState):

    def update(self, keys, controller) -> None:
        """
        Updates the players state, includes player movement and state switching
        :param keys: The pygame input keys
        :param controller: The controller instance
        """

        # Create an instance of GameControls
        game_controls = GameControls()

        if game_controls.get_movement_vector(keys, controller) != pygame.Vector2(0, 0):
            self.player.state = self.player.moving_state_inst
        elif keys[game_controls.key_sprint]:
            self.player.state = self.player.sprinting_state_inst
        else:
            self.player.stats.current_stamina += 2.0
            self.player.stats.current_stamina = min(self.player.stats.current_stamina, self.player.stats.max_stamina)

    def draw(self) -> None:
        """
        Changes the sprite for the character depending on the state
        """
        self.player.sprite.image = self.player.sprite.frames[0]
