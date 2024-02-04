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

        self._button_down_since_last_attack = False

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
            "slash": Animation(1000/self.weapon.attack_speed, PNGSprite.make_from_sprite_sheet('Sprites/slash.png', 40, 120)),
            "walk": Animation(1000, PNGSprite.make_from_sprite_sheet('Sprites/sprite_sheet.png', 32, 32)),
            "sprint": Animation(750, PNGSprite.make_from_sprite_sheet('Sprites/sprite_sheet.png', 32, 32)),
            "walk_side": Animation(1000, PNGSprite.make_from_sprite_sheet('Sprites/walk_side.png', 32, 32)),
            "sprint_side": Animation(750, PNGSprite.make_from_sprite_sheet('Sprites/walk_side.png', 32, 32))
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

        self.update_attack(left_mouse, game_controller)
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

    def update_attack(self, left_mouse, game_controller):
        # Only show the slash when attacking

        # TODO: Fix Slash's First Frame shows

        # Animation Type Diff
        if left_mouse or game_controller.check_user_input(Input.ATTACK):
            if not self._button_down_since_last_attack:
                if self.cooldown_timers.dodge.has_seconds_passed(1 / self.weapon.attack_speed):
                    self.animations["slash"].start_animation()
                    # Store last dodge time
                    self.cooldown_timers.dodge.restart_time()
                    self._button_down_since_last_attack = True
        else:
            self._button_down_since_last_attack = False

        # Animation Type Diff
        if self.animations["slash"].start_time is not None:
            _elapsed_time = get_ticks() - self.animations["slash"].start_time
        else:
            _elapsed_time = 0

        # Run the animation and get the current frame
        self.animations["slash"].run_once(_elapsed_time)

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
        self.rotate_around_player_center(self.game_obj["block"], self.left_angle, 50.0)
        self.rotate_around_player_center(self.animations["slash"], self.left_angle, 30.0)

    def set_relative_position(self, offset):
        self.relative_position = self.position + offset

    @staticmethod
    def get_mouse_relative_angle(mouse_pos, image_center) -> float:
        # Get the mouse position
        dx, dy = mouse_pos - image_center
        target_angle = (math.degrees(math.atan2(dx, dy)) + 360) % 360

        return target_angle

    def rotate_around_player_center(
        self, game_object: GameObject | Animation, angle: float, offset: float
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
        offset_vector = Vector2(
            offset * math.sin(math.radians(angle)),
            offset * math.cos(math.radians(angle)),
        )

        # Grab the half of the size of the player
        player_half_size = Vector2(
            self.game_obj["player"].sprite.image.get_width() // 2,
            self.game_obj["player"].sprite.image.get_height() // 2
        )

        # Grab half of the size of the object
        obj_half_size = Vector2(
            game_object.sprite.image.get_width() // 2,
            game_object.sprite.image.get_height() // 2,
        )

        full_offset = player_half_size - obj_half_size + offset_vector

        game_object.position = self.position + full_offset
