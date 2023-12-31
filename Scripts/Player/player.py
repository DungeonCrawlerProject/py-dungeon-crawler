import math
from dataclasses import dataclass

import pygame

from Scripts.Player.Movement.player_stats import PlayerStats
from Scripts.Player.PlayerStateMachine.player_state import IdleState


# TODO Position is temp
@dataclass
class Position:
    x: float
    y: float


class Player:
    position: Position
    stats: PlayerStats = PlayerStats()
    angle: float = 0

    def __init__(self):
        # Note: the real state should be Idle once statemachine is added properly
        self.state = IdleState(self)
        self.mouse_position = (0, 0)

    def update(self, keys) -> None:
        # currentState = currentState.DoState(this);
        self.mouse_position = pygame.mouse.get_pos()

        self.state.update(keys)

        # TODO un_hardcode, Should be fixed update
        player_size = 50

        # currentState = currentState.DoState(this);
        self.mouse_position = pygame.mouse.get_pos()

        # Get the mouse position
        mouse_x, mouse_y = self.mouse_position

        self.angle = math.degrees(
            math.atan2(
                mouse_y - (self.position.y + player_size // 2),
                mouse_x - (self.position.x + player_size // 2)
            )
        )

    def take_damage(self, damage: float):
        self.stats.current_health -= damage

        # healthBar.SetHealth(curHealth / maxHealth);

        if self.stats.current_health < 0:
            self.kill_player()

    def kill_player(self):
        raise NotImplementedError

    def draw(self, screen):
        self.state.draw(screen)
