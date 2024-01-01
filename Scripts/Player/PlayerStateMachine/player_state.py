"""
Player State Machine
By: Sean McClanahan
Last Modified: 12/31/2023
"""


import math
from abc import ABC, abstractmethod
import time

import pygame


class IPlayerState(ABC):
    def __init__(self, player) -> None:
        self.player = player

    @abstractmethod
    def update(self, keys):
        pass

    @abstractmethod
    def draw(self, screen):
        pass


class DodgeState(IPlayerState):

    def __init__(self, player) -> None:
        super().__init__(player)

    def update(self, keys):
        if not keys[pygame.K_SPACE]:
            self.player.state = IdleState(self.player)
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

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 255), (self.player.position.x, self.player.position.y, 50, 50))


class IdleState(IPlayerState):
    def update(self, keys):
        if keys[pygame.K_w] or keys[pygame.K_a] or keys[pygame.K_s] or keys[pygame.K_d]:
            self.player.state = MovingState(self.player)
        elif keys[pygame.K_SPACE]:
            self.player.state = DodgeState(self.player)
        elif keys[pygame.K_LSHIFT]:
            self.player.state = SprintingState(self.player)

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.player.position.x, self.player.position.y, 50, 50))


class MovingState(IPlayerState):
    def update(self, keys):
        if not (keys[pygame.K_w] or keys[pygame.K_a] or keys[pygame.K_s] or keys[pygame.K_d]):
            self.player.state = IdleState(self.player)
        elif keys[pygame.K_SPACE]:
            self.player.state = DodgeState(self.player)
        elif keys[pygame.K_LSHIFT]:
            self.player.state = SprintingState(self.player)
        else:
            self.move(keys)

    def move(self, keys):
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

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), (self.player.position.x, self.player.position.y, 50, 50))


class SprintingState(IPlayerState):
    def update(self, keys):
        if not keys[pygame.K_LSHIFT]:
            self.player.state = IdleState(self.player)
        else:
            self.move(keys)

    def move(self, keys):
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

        self.player.position.x += self.player.stats.speed * movement_input.x * self.player.stats.sprint_factor / mag
        self.player.position.y += self.player.stats.speed * movement_input.y * self.player.stats.sprint_factor / mag

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 0), (self.player.position.x, self.player.position.y, 50, 50))
