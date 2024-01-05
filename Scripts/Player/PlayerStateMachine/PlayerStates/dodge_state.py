import math
import time

import pygame

from Scripts.Player.PlayerStateMachine.player_state import IPlayerState


class DodgeState(IPlayerState):

    def __init__(self, player) -> None:
        super().__init__(player)

    def update(self, keys):
        if not keys[pygame.K_SPACE]:
            self.player.state = self.player.idle_state_inst
        else:
            self.dodge(keys)

    def dodge(self, keys):

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

    def draw(self):
        self.player.sprite.image = self.player.sprite.frames[3]
