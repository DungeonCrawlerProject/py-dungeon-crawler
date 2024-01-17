"""
Walking State
By: Sean McClanahan
Last Modified: 01/04/2024
"""

import math
import time

import pygame

from Scripts.Player.PlayerStateMachine.player_state import IPlayerState


class MovingState(IPlayerState):

    def update(self, keys) -> None:
        """
        Updates the players state, includes player movement and state switching
        :param keys: The pygame input keys
        """

        dt = time.perf_counter() - self.player.cooldown_timers.dodge_cooldown_timer

        if not (keys[pygame.K_w] or keys[pygame.K_a] or keys[pygame.K_s] or keys[pygame.K_d]):
            self.player.state = self.player.idle_state_inst
        elif keys[pygame.K_SPACE] and dt >= self.player.stats.dodge_cooldown:
            self.player.state = self.player.dodge_state_inst
        elif keys[pygame.K_LSHIFT]:
            self.player.state = self.player.sprinting_state_inst
        else:
            self.player.stats.current_stamina += 1.5
            self.player.stats.current_stamina = min(self.player.stats.current_stamina, self.player.stats.max_stamina)
            self.move(keys)

    def move(self, keys) -> None:
        """
        Moves the player quickly
        :param keys: The keys from pygame to determine direction
        """

        movement_input = pygame.Vector2(0, 0)

        if keys[pygame.K_w]:
            movement_input.y = -1
        if keys[pygame.K_s]:
            movement_input.y = 1
        if keys[pygame.K_a]:
            movement_input.x = -1
        if keys[pygame.K_d]:
            movement_input.x = 1

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
