"""
Dodge State
By: Sean McClanahan
Last Modified: 01/27/2024
"""

import math

from Scripts.Utility.input import Input
from Scripts.Utility.game_controller import GameController
from Scripts.Player.PlayerStateMachine.player_state import IPlayerState


class DodgeState(IPlayerState):

    def update(self, game_controller: GameController) -> None:
        """
        Updates the players state, includes player movement and state switching
        :param game_controller: The Game Controller Instance
        """

        if game_controller.check_user_input(Input.DODGE) and self.player.cooldown_timers.dodge.has_seconds_passed(self.player.stats.dodge_cooldown):
            self.dodge(game_controller)
        elif game_controller.is_moving():
            self.player.state = self.player.moving_state_inst
        else:
            self.player.state = self.player.idle_state_inst

    def dodge(self, game_controller: GameController) -> None:
        """
        Performs a dodge
        :param game_controller: The Game Controller Instance
        """

        # Use the movement input from the MovingState
        movement_input = game_controller.get_movement_vector()

        mag = math.sqrt(movement_input.x ** 2 + movement_input.y ** 2)
        mag = max(1.0, mag)

        self.player.position.x += self.player.stats.dodge_distance * movement_input.x / mag
        self.player.position.y += self.player.stats.dodge_distance * movement_input.y / mag

        # Store last dodge time
        self.player.cooldown_timers.dodge.restart_time()

    def draw(self) -> None:
        """
        Changes the sprite for the character depending on the state
        """
        self.player.game_obj["player"].sprite.change_frame(3)
