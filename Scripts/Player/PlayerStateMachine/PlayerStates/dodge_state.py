"""
Dodge State
By: Sean McClanahan
Last Modified: 01/27/2024
"""

import math
import time

from GameData.game_controls import GameControls
from Scripts.Player.PlayerStateMachine.player_state import IPlayerState


class DodgeState(IPlayerState):

    def update(self, game_controller: GameControls) -> None:
        """
        Updates the players state, includes player movement and state switching
        :param game_controller: The Game Controller Instance
        """

        dt = time.perf_counter() - self.player.cooldown_timers.dodge_cooldown_timer

        if (game_controller.input_key[game_controller.key_dodge] or game_controller.input_btn.get_button(game_controller.btn_dodge)) and dt >= self.player.stats.dodge_cooldown:
            self.dodge(game_controller)
        elif any(game_controller.input_key[key] for key in game_controller.key_movement):
            self.player.state = self.player.moving_state_inst
        else:
            self.player.state = self.player.idle_state_inst

    def dodge(self, game_controller: GameControls) -> None:
        """
        Performs a dodge
        :param game_controller: The Game Controller Instance
        """

        current_time = time.perf_counter()
        if current_time - self.player.cooldown_timers.dodge_cooldown_timer < self.player.stats.dodge_cooldown:
            return

        # Use the movement input from the MovingState
        movement_input = game_controller.get_movement_vector()

        mag = math.sqrt(movement_input.x ** 2 + movement_input.y ** 2)
        mag = max(1.0, mag)

        self.player.position.x += self.player.stats.dodge_distance * movement_input.x / mag
        self.player.position.y += self.player.stats.dodge_distance * movement_input.y / mag

        # Store last dodge time
        self.player.cooldown_timers.dodge_cooldown_timer = current_time

    def draw(self) -> None:
        """
        Changes the sprite for the character depending on the state
        """
        self.player.sprite.image = self.player.sprite.frames[3]
