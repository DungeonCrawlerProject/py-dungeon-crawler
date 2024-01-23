"""
Dodge State
By: Sean McClanahan
Last Modified: 01/04/2024
"""

import math
import time

import pygame

from GameData.game_controls import GameControls
from Scripts.Player.PlayerStateMachine.player_state import IPlayerState


class DodgeState(IPlayerState):

    def update(self, keys) -> None:
        """
        Updates the players state, includes player movement and state switching
        :param keys: The pygame input keys
        """

        dt = time.perf_counter() - self.player.cooldown_timers.dodge_cooldown_timer

        # Create an instance of GameControls
        game_controls = GameControls()

        if keys[game_controls.key_dodge] and dt >= self.player.stats.dodge_cooldown:
            self.dodge(keys)
        elif any(keys[key] for key in game_controls.key_movement):
            self.player.state = self.player.moving_state_inst
        else:
            self.player.state = self.player.idle_state_inst

    def dodge(self, keys) -> None:
        """
        Performs a dodge
        :param keys: The keys from pygame to determine direction
        """

        current_time = time.perf_counter()
        if current_time - self.player.cooldown_timers.dodge_cooldown_timer < self.player.stats.dodge_cooldown:
            return

        # Use the movement input from the MovingState
        movement_input = pygame.Vector2(0, 0)
        if keys[pygame.K_w]:
            movement_input.y = -1
        if keys[pygame.K_s]:
            movement_input.y = 1
        if keys[pygame.K_a]:
            movement_input.x = -1
        if keys[pygame.K_d]:
            movement_input.x = 1

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
