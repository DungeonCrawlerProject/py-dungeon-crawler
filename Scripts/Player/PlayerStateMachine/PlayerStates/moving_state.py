"""
Walking State
By: Sean McClanahan
Last Modified: 01/27/2024
"""

import math
import time

import pygame

from GameData.game_controls import GameControls
from Scripts.Player.PlayerStateMachine.player_state import IPlayerState


class MovingState(IPlayerState):

    def update(self, game_controller: GameControls) -> None:
        """
        Updates the players state, includes player movement and state switching
        :param game_controller: The Game Controller Instance
        """

        dt = time.perf_counter() - self.player.cooldown_timers.dodge_cooldown_timer

        if game_controller.get_movement_vector() == pygame.Vector2(0, 0):
            self.player.state = self.player.idle_state_inst
        elif (game_controller.input_key[game_controller.key_dodge] or game_controller.input_btn.get_button(game_controller.btn_dodge)) and dt >= self.player.stats.dodge_cooldown:
            self.player.state = self.player.dodge_state_inst
        elif game_controller.input_key[game_controller.key_sprint]:
            self.player.state = self.player.sprinting_state_inst
        else:
            self.player.stats.current_stamina += 1.5
            self.player.stats.current_stamina = min(self.player.stats.current_stamina, self.player.stats.max_stamina)
            self.move(game_controller)

    def move(self, game_controller: GameControls) -> None:
        """
        Moves the player quickly
        :param game_controller: The Game Controller Instance
        """

        movement_input = game_controller.get_movement_vector()

        # Take max of that and 1 to prevent zero division error
        mag = math.sqrt(movement_input.x ** 2 + movement_input.y ** 2)
        mag = max(1.0, mag)

        self.player.position.x += self.player.stats.speed * movement_input.x / mag
        self.player.position.y += self.player.stats.speed * movement_input.y / mag

    def draw(self) -> None:
        """
        Changes the sprite for the character depending on the state
        """
        self.player.sprite.image = self.player.sprite.frames[1]
