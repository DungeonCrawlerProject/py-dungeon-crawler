"""
Idle State
By: Sean McClanahan
Last Modified: 01/04/2024
"""

import pygame

from Scripts.Player.PlayerStateMachine.player_state import IPlayerState


class IdleState(IPlayerState):
    def update(self, keys) -> None:
        """
        Updates the players state, includes player movement and state switching
        :param keys: The pygame input keys
        """

        if keys[pygame.K_w] or keys[pygame.K_a] or keys[pygame.K_s] or keys[pygame.K_d]:
            self.player.state = self.player.moving_state_inst
        elif keys[pygame.K_LSHIFT]:
            self.player.state = self.player.sprinting_state_inst
        else:
            self.player.stats.current_stamina += 2.0
            self.player.stats.current_stamina = min(self.player.stats.current_stamina, self.player.stats.max_stamina)

    def draw(self) -> None:
        """
        Changes the sprite for the character depending on the state
        """
        self.player.sprite.image = self.player.sprite.frames[0]
