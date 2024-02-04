"""
The player class
By: Sean McClanahan and Nick Petruccelli
Last Modified: 02/03/2024
"""

import math
from typing import (
    Optional,
    Tuple
)

from pygame import Vector2
from pygame.time import get_ticks

from Scripts.CollisionBox.collision_box import CollisionBox
from Scripts.GameObject.game_object import GameObject
from Scripts.Player.Actions.action import Action
from Scripts.Player.PlayerStateMachine.PlayerStates.dodge_state import DodgeState
from Scripts.Player.PlayerStateMachine.PlayerStates.idle_state import IdleState
from Scripts.Player.PlayerStateMachine.PlayerStates.moving_state import MovingState
from Scripts.Player.PlayerStateMachine.PlayerStates.sprinting_state import SprintingState
from Scripts.Player.Stats.player_cooldowns import PlayerCoolDownTimer
from Scripts.Player.Stats.player_stats import PlayerStats
from Scripts.Player.Weapons.weapon import Weapon
from Scripts.Utility.game_controller import GameController
from Scripts.Utility.input import Input
from Scripts.animation import Animation
from Scripts.sprite import PNGSprite

ROTATE_SPEED = 50


class Player:

    def __init__(
        self, initial_position: Vector2, camera, collision_handler
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

        self.weapon = Weapon(3)

        # TODO THIS IS A TERRIBLE PRACTICE
        self.known_enemies = []

        # Dataclasses
        self.stats = PlayerStats()
        self.cooldown_timers = PlayerCoolDownTimer()

        # The player's state, Store the states' instances to prevent circular imports
        self.idle_state_inst = IdleState(self)
        self.moving_state_inst = MovingState(self)
        self.sprinting_state_inst = SprintingState(self)
        self.dodge_state_inst = DodgeState(self)
        self.state = self.idle_state_inst
        self._memory_attack_angle = Vector2(0, 0)

        # Store and Make Player Objects
        self.game_obj = {
            "player": GameObject(self.position, PNGSprite.make_from_sprite_sheet('Sprites/sprite_sheet.png', 32, 32), tag="player_idle"),
            "block": GameObject(self.position, PNGSprite.make_single_sprite('Sprites/block.png'))
        }

        self.animations = {
            "walk": Animation(1000, PNGSprite.make_from_sprite_sheet('Sprites/sprite_sheet.png', 32, 32)),
            "sprint": Animation(750, PNGSprite.make_from_sprite_sheet('Sprites/sprite_sheet.png', 32, 32)),
            "walk_side": Animation(1000, PNGSprite.make_from_sprite_sheet('Sprites/walk_side.png', 32, 32)),
            "sprint_side": Animation(750, PNGSprite.make_from_sprite_sheet('Sprites/walk_side.png', 32, 32))
        }

        self.actions = {
            "slash": Action(Animation(1000/self.weapon.attack_speed, PNGSprite.make_from_sprite_sheet('Sprites/slash.png', 40, 120)), 0.0)
        }

        self.animations["walk"].sprite.frames.pop(0)
        self.animations["walk_side"].sprite.frames.pop(0)

        # Set All Animations Invisible on Start up
        for anim in self.animations.values():
            anim.sprite.visible = False

        # Give the player the camera
        self.add_camera(camera)

        # Add collision box
        dimensions = Vector2(14, 30)
        self.collider = CollisionBox(
            parent=self,
            position=initial_position - Vector2(16, 16),
            dimensions=dimensions,
            collision_handler=collision_handler,
            tag="player",
        )

    def update(
        self,
        game_controller: GameController,
        mouse_buttons: Tuple[bool, bool, bool],
        mouse_pos: Optional[Tuple[float, float]],
    ) -> None:
        """
        Updates the player object
        :param game_controller: The Game Controller Instance
        :param mouse_buttons: Booleans representing whether each button on a mouse is pressed.
        :param mouse_pos: The position of the mouse
        """
        # Check if the player is dead
        if self.stats.current_health <= 0:
            self.kill_player()
            return

        # Update State-machine and Sprite Based Hit-box
        self.game_obj["player"].sprite.rect.x, self.game_obj["player"].sprite.rect.y = self.position.xy - Vector2(16, 16)

        self.game_obj["player"].sprite.visible = True

        for anim in self.animations.values():
            anim.position = self.position

        self.state.update(game_controller)

        left_mouse, middle_mouse, right_mouse = mouse_buttons

        self.update_attack(game_controller)
        self.update_block(right_mouse, game_controller)

        # Cursor Rotation
        target_angle = self.get_mouse_relative_angle(mouse_pos, self.relative_position)

        # Set Right and Left Angle Logic
        self.left_angle = self.get_left_angle(game_controller)
        self.right_angle += ROTATE_SPEED * math.sin(
            math.radians(target_angle - self.right_angle)
        )
        self.right_angle %= 360

        # Update collider
        self.collider.x = self.position.x
        self.collider.y = self.position.y
        self.check_collisions()

        # Change player pos
        self.draw()

    def update_attack(self, game_controller):

        # If the Attack Button is Pressed, attempt the action
        if game_controller.is_unique_left_click() or game_controller.check_user_input(Input.ATTACK):
            self.actions["slash"].attempt()

        self.actions["slash"].draw()

    def update_block(self, right_mouse, game_controller):
        # Only show the block when blocking
        if right_mouse or game_controller.check_user_input(Input.BLOCK):
            self.game_obj["block"].sprite.visible = True
        else:
            self.game_obj["block"].sprite.visible = False

    def check_collisions(self):
        pass

    def get_left_angle(self, game_controller) -> float:
        """
        Returns the angle from WASD keyboard input
        :param game_controller: The Game Controller Instance
        :return: The angle is degrees
        """

        # Create an instance of GameControls
        mov_dir = game_controller.get_movement_vector()

        # Default down
        if not game_controller.is_moving():
            mov_dir.x, mov_dir.y = (
                self._memory_attack_angle.x,
                self._memory_attack_angle.y,
            )
        else:
            self._memory_attack_angle.x, self._memory_attack_angle.y = (
                mov_dir.x,
                mov_dir.y,
            )

        return math.degrees(math.atan2(mov_dir.x, mov_dir.y))

    def add_camera(self, camera):
        """
        Adds a camera instance to the player.
        :param camera: The camera instance
        :return:
        """

        camera.game_objects.extend(self.game_obj.values())
        camera.game_objects.extend(self.animations.values())
        camera.game_objects.append(self.actions["slash"].animation)
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
        self.game_obj["player"].sprite.visible = False

        for obj in self.game_obj.values():
            obj.sprite.visible = False

    def draw(self) -> None:
        self.state.draw()

        # Update the rotate functions
        self.actions["slash"].animation.rotate_about_object_center(self.game_obj["player"], self.left_angle, 30.0)
        self.game_obj["block"].rotate_about_object_center(self.game_obj["player"], self.left_angle, 30.0)

    def set_relative_position(self, offset):
        self.relative_position = self.position + offset

    @staticmethod
    def get_mouse_relative_angle(mouse_pos, image_center) -> float:
        # Get the mouse position
        dx, dy = mouse_pos - image_center
        target_angle = (math.degrees(math.atan2(dx, dy)) + 360) % 360

        return target_angle
