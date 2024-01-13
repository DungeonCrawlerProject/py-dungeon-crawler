"""
The player class
By: Sean McClanahan and Nick Petruccelli
Last Modified: 01/13/2024
"""

import math
from typing import (
    Optional,
    Tuple
)

import pygame

from Scripts.Player.PlayerStateMachine.PlayerStates.dodge_state import DodgeState
from Scripts.Player.PlayerStateMachine.PlayerStates.idle_state import IdleState
from Scripts.Player.PlayerStateMachine.PlayerStates.moving_state import MovingState
from Scripts.Player.PlayerStateMachine.PlayerStates.sprinting_state import SprintingState
from Scripts.Player.Stats.player_cooldowns import PlayerCoolDownTimer
from Scripts.Player.Stats.player_stats import PlayerStats
from Scripts.sprite import PNGSprite
from Scripts.GameObject.game_object import GameObject

ROTATE_SPEED = 50


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
        self.relative_position = initial_position
        self.hit_box = pygame.Vector2(50, 50)
        self.angle = 0.0
        self.mouse_position = (0, 0)

        # Dataclasses
        self.stats = PlayerStats()
        self.cooldown_timers = PlayerCoolDownTimer()

        # TODO: Make State Machine For Combat
        self.combat_color_cursor = (0, 0, 0)

        # The player's state, Store the states' instances to prevent circular imports
        self.idle_state_inst = IdleState(self)
        self.moving_state_inst = MovingState(self)
        self.sprinting_state_inst = SprintingState(self)
        self.dodge_state_inst = DodgeState(self)
        self.state = self.idle_state_inst

        # Make the sprite in the center
        sprite_sheet = pygame.image.load('Sprites/sprite_sheet.png').convert_alpha()
        self.sprite = PNGSprite.make_from_sprite_sheet(sprite_sheet, 32, 64)

        # TODO SEPARATE THIS
        self.arrow = PNGSprite.make_from_sprite_sheet(pygame.image.load('Sprites/arrow.png').convert_alpha(), 25, 79)

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

        # Cursor Rotation
        target_angle = self.get_mouse_relative_angle(mouse_pos, self.relative_position)
        self.angle += ROTATE_SPEED * math.sin(math.radians(target_angle - self.angle))
        self.angle %= 360

        self.draw()

    def add_camera(self, camera):
        camera.game_objects.extend(
            [
                GameObject(self.position, self.sprite),
                GameObject(self.position, self.arrow)
            ]
        )
        camera.position = self.position.copy()

    def take_damage(self, damage: float) -> None:
        self.stats.current_health -= damage

        # healthBar.SetHealth(curHealth / maxHealth);

        if self.stats.current_health < 0:
            self.kill_player()

    def kill_player(self) -> None:
        raise NotImplementedError

    def draw(self) -> None:

        self.state.draw()
        self.arrow.rotate(self.angle)

    def set_relative_position(self, x, y):

        self.relative_position = self.position + pygame.Vector2(x, y)

    @staticmethod
    def get_mouse_relative_angle(mouse_pos, image_center) -> float:

        # Get the mouse position
        dx, dy = mouse_pos - image_center
        target_angle = (math.degrees(math.atan2(dx, dy)) + 360) % 360

        return target_angle
