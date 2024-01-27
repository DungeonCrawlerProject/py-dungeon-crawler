"""
Dodge State
By: Sean McClanahan
Last Modified: 01/04/2024
"""

import math
import time

from GameData.game_controls import GameControls
from Scripts.Player.PlayerStateMachine.player_state import IPlayerState


class DodgeState(IPlayerState):

    def update(self, keys, controller) -> None:
        """
        Updates the players state, includes player movement and state switching
        :param keys: The pygame input keys
        :param controller: The controller instance
        """

        dt = time.perf_counter() - self.player.cooldown_timers.dodge_cooldown_timer

        # Create an instance of GameControls
        game_controls = GameControls()



        if (keys[game_controls.key_dodge] or controller.get_button(game_controls.btn_dodge)) and dt >= self.player.stats.dodge_cooldown:
            self.dodge(keys, controller)
        elif any(keys[key] for key in game_controls.key_movement):
            self.player.state = self.player.moving_state_inst
        else:
            self.player.state = self.player.idle_state_inst

    def dodge(self, keys, controller) -> None:
        """
        Performs a dodge
        :param keys: The keys from pygame to determine direction
        :param controller: The controller instance
        """

        current_time = time.perf_counter()
        if current_time - self.player.cooldown_timers.dodge_cooldown_timer < self.player.stats.dodge_cooldown:
            return

        # Create an instance of GameControls
        game_controls = GameControls()

        # Use the movement input from the MovingState
        movement_input = game_controls.get_movement_vector(keys, controller)

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
