"""
The player class
By: Sean McClanahan and Nick Petruccelli
Last Modified: 12/31/2023
"""

import math
from typing import (
    Optional,
    Tuple
)

import pygame

from Scripts.Player.Stats.player_cooldowns import PlayerCoolDownTimer
from Scripts.Player.Stats.player_stats import PlayerStats
from Scripts.Player.PlayerStateMachine.player_state import IdleState
from Scripts.sprite import PNGSprite


class Player:

    def __init__(
            self,
            initial_position: pygame.Vector2,
            camera
    ) -> None:
        """
        The player is the controllable character for the user.
        :param initial_position: The position to first place the player.
        :param camera: The instance of the camera
        """

        # Positional Variables
        self.position = initial_position
        self.hit_box = pygame.Vector2(50, 50)
        self.angle = 0.0
        self.mouse_position = (0, 0)

        # Dataclasses
        self.stats = PlayerStats()
        self.cooldown_timers = PlayerCoolDownTimer()

        # TODO: Make State Machine For Combat
        self.combat_color_cursor = (0, 0, 0)

        # The player's state
        self.state = IdleState(self)

        # Make the sprite in the center
        self.sprite = PNGSprite(camera)

        # Give the player the camera
        self.add_camera(camera)

    def update(
            self,
            keys: pygame.key.ScancodeWrapper,
            mouse_buttons: Tuple[bool, bool, bool],
            mouse_pos: Optional[Tuple[float, float]]
    ) -> None:
        """
        Updates the player object
        :param keys: The keybindings
        :param mouse_buttons: Booleans representing whether each button on a mouse is pressed.
        :param mouse_pos: The position of the mouse
        """

        self.mouse_position = mouse_pos

        self.state.update(keys)

        left_mouse, middle_mouse, right_mouse = mouse_buttons

        if left_mouse:
            self.combat_color_cursor = (255, 0, 0)
        elif right_mouse:
            self.combat_color_cursor = (0, 255, 0)
        else:
            self.combat_color_cursor = (0, 0, 0)

        if mouse_pos:
            # Get the mouse position
            mouse_x, mouse_y = self.mouse_position

            self.angle = math.degrees(
                math.atan2(
                    mouse_y - (self.position.y + self.hit_box[1] // 2),
                    mouse_x - (self.position.x + self.hit_box[0] // 2)
                )
            )

    def add_camera(self, camera):
        camera.add(self.sprite)
        camera.position = self.position.copy()

    def take_damage(self, damage: float) -> None:
        self.stats.current_health -= damage

        # healthBar.SetHealth(curHealth / maxHealth);

        if self.stats.current_health < 0:
            self.kill_player()

    def kill_player(self) -> None:
        raise NotImplementedError

    def draw(self, screen) -> None:
        self.state.draw(screen)

        # Draw the players line of direction
        pygame.draw.circle(
            surface=screen,
            color=self.combat_color_cursor,
            center=(
                math.cos(math.radians(self.angle)) * 100 + self.position.x + self.hit_box.x / 2,
                math.sin(math.radians(self.angle)) * 100 + self.position.y + self.hit_box.y / 2
            ),
            radius=15,
            width=5
        )
