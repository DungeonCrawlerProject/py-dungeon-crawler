"""
Sprint State
By: Sean McClanahan
Last Modified: 01/27/2024
"""

import math

from Scripts.Utility.game_controller import GameController
from Scripts.Player.PlayerStateMachine.player_state import IPlayerState


class SprintingState(IPlayerState):

    def update(self, game_controller: GameController) -> None:
        """
        Updates the players state, includes player movement and state switching
        :param game_controller: The Game Controller Instance
        """

        if True:
            self.player.state = self.player.idle_state_inst

    def move(self, game_controller: GameController) -> None:
        """
        Moves the player quickly
        :param game_controller: The Game Controller Instance
        """

        # Create an instance of GameControls
        movement_input = game_controller.get_movement_vector()

        # Take max of that and 1 to prevent zero division error
        mag = math.sqrt(movement_input.x ** 2 + movement_input.y ** 2)
        mag = max(1.0, mag)

        self.player.position.x += self.player.stats.speed * movement_input.x * self.player.stats.sprint_factor / mag
        self.player.position.y += self.player.stats.speed * movement_input.y * self.player.stats.sprint_factor / mag

    def draw(self):
        """
        Changes the sprite for the character depending on the state
        """
        self.player.sprite.image = self.player.sprite.frames[2]
