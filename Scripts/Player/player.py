"""
The player class
By: Sean McClanahan and Nick Petruccelli
Last Modified: 01/15/2024
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
        self.left_angle = 0.0
        self.right_angle = 0.0

        # Dataclasses
        self.stats = PlayerStats()
        self.cooldown_timers = PlayerCoolDownTimer()

        # The player's state, Store the states' instances to prevent circular imports
        self.idle_state_inst = IdleState(self)
        self.moving_state_inst = MovingState(self)
        self.sprinting_state_inst = SprintingState(self)
        self.dodge_state_inst = DodgeState(self)
        self.state = self.idle_state_inst

        # Make the sprite in the center
        sprite_sheet = pygame.image.load('Sprites/sprite_sheet.png').convert_alpha()
        self.sprite = PNGSprite.make_from_sprite_sheet(sprite_sheet, 32, 64)

        # Store and Make Player Objects
        self.player_objects = {
            "player_sprite": GameObject(self.position, self.sprite),
            "arrow_sprite": GameObject(self.position, PNGSprite.make_single_sprite('Sprites/arrow.png')),
            "slash_sprite": GameObject(self.position, PNGSprite.make_single_sprite('Sprites/slash.png')),
            "block_sprite": GameObject(self.position, PNGSprite.make_single_sprite('Sprites/block.png'))
        }

        # Set Arrow Invisible
        self.player_objects["arrow_sprite"].sprite.visible = False

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

        self.state.update(keys)

        left_mouse, middle_mouse, right_mouse = mouse_buttons

        # Only show the slash when attacking
        if left_mouse:
            self.player_objects["slash_sprite"].sprite.visible = True
        else:
            self.player_objects["slash_sprite"].sprite.visible = False

        # Only show the block when blocking
        if right_mouse:
            self.player_objects["block_sprite"].sprite.visible = True
        else:
            self.player_objects["block_sprite"].sprite.visible = False

        # Cursor Rotation
        target_angle = self.get_mouse_relative_angle(mouse_pos, self.relative_position)

        # Set Right and Left Angle Logic
        self.left_angle = self.get_left_angle(keys)
        self.right_angle += ROTATE_SPEED * math.sin(math.radians(target_angle - self.right_angle))
        self.right_angle %= 360

        # Change player pos
        self.draw()

    @staticmethod
    def get_left_angle(keys) -> float:
        """
        Returns the angle from WASD keyboard input
        :param keys: Keyboard pygame key event
        :return: The angle is degrees
        """

        mov_dir = pygame.Vector2(0, 0)

        if keys[pygame.K_w]:
            mov_dir.y = 1
        if keys[pygame.K_s]:
            mov_dir.y = -1
        if keys[pygame.K_a]:
            mov_dir.x = -1
        if keys[pygame.K_d]:
            mov_dir.x = 1

        # Default down
        if not (keys[pygame.K_w] or keys[pygame.K_a] or keys[pygame.K_s] or keys[pygame.K_d]):
            mov_dir.x, mov_dir.y = 0, -1

        return math.degrees(math.atan2(mov_dir.x, -mov_dir.y))

    def add_camera(self, camera):
        """
        Adds a camera instance to the player.
        :param camera: The camera instance
        :return:
        """

        camera.game_objects.extend(self.player_objects.values())
        camera.position = self.position.copy()

    def take_damage(self, damage: float) -> None:
        """
        Deals damage to the player
        :param damage: The damage
        """

        self.stats.current_health -= damage

        if self.stats.current_health < 0:
            self.kill_player()

    def kill_player(self) -> None:
        raise NotImplementedError

    def draw(self) -> None:

        self.state.draw()

        # Update the rotate functions
        self.rotate_around_player_center(self.player_objects["arrow_sprite"], self.left_angle, 200.0)
        self.rotate_around_player_center(self.player_objects["block_sprite"], self.left_angle, 50.0)
        self.rotate_around_player_center(self.player_objects["slash_sprite"], self.left_angle, 30.0)

    def set_relative_position(self, offset):

        self.relative_position = self.position + offset

    @staticmethod
    def get_mouse_relative_angle(mouse_pos, image_center) -> float:

        # Get the mouse position
        dx, dy = mouse_pos - image_center
        target_angle = (math.degrees(math.atan2(dx, dy)) + 360) % 360

        return target_angle

    def rotate_around_player_center(
            self,
            game_object: GameObject,
            angle: float,
            offset: float
    ) -> None:
        """
        Updates the position and angle of a game object owned by the player
        :param game_object: The object to rotate about the player
        :param angle: The angle of the object in degrees
        :param offset: The distance between the objects center and the player's center
        """

        # Rotate the object first to prevent bouncy animation
        game_object.sprite.rotate(angle)

        # Get the offset for the object
        offset_vector = pygame.Vector2(
            offset * math.sin(math.radians(angle)),
            offset * math.cos(math.radians(angle))
        )

        # Grab the half of the size of the player
        player_half_size = pygame.Vector2(
            self.sprite.image.get_width() // 2,
            self.sprite.image.get_height() // 2
        )

        # Grab half of the size of the object
        obj_half_size = pygame.Vector2(
            game_object.sprite.image.get_width() // 2,
            game_object.sprite.image.get_height() // 2
        )

        full_offset = player_half_size - obj_half_size + offset_vector

        game_object.position = self.position + full_offset
