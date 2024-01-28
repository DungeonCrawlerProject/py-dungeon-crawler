"""
Idle State
By: Sean McClanahan
Last Modified: 01/27/2024
"""

import pygame

from GameData.game_controls import GameControls
from Scripts.Player.PlayerStateMachine.player_state import IPlayerState


class IdleState(IPlayerState):

    def update(self, game_controller: GameControls) -> None:
        """
        Updates the players state, includes player movement and state switching
        :param game_controller: The Game Controller Instance
        """

        if game_controller.get_movement_vector() != pygame.Vector2(0, 0):
            self.player.state = self.player.moving_state_inst
        elif game_controller.input_key[game_controller.key_sprint]:
            self.player.state = self.player.sprinting_state_inst
        else:
            self.player.stats.current_stamina += 2.0
            self.player.stats.current_stamina = min(self.player.stats.current_stamina, self.player.stats.max_stamina)

    def draw(self) -> None:
        """
        Changes the sprite for the character depending on the state
        """
        self.player.sprite.image = self.player.sprite.frames[0]
