"""
Walking State
By: Sean McClanahan
Last Modified: 01/27/2024
"""

import math

from pygame import Vector2

from Scripts.Player.PlayerStateMachine.player_state import IPlayerState
from Scripts.Utility.cronos_clock import CronosClock
from Scripts.Utility.game_controller import GameController
from Scripts.Utility.input import Input


class MovingState(IPlayerState):
    move_dir = Vector2(0, 0)
    momentum_timer = CronosClock()
    momentum_memory = Vector2(0, 0)

    def update(self, game_controller: GameController) -> None:
        """
        Updates the players state, includes player movement and state switching
        :param game_controller: The Game Controller Instance
        """
        self.move_dir = game_controller.get_movement_vector()

        if not game_controller.is_moving():
            self.player.animations["walk"].stop()
            self.player.animations["walk_side"].stop()

        if self.momentum_timer.has_seconds_passed(3.0):
            self.player.state = self.player.sprinting_state_inst

            self.player.animations["walk"].stop()
            self.player.animations["walk_side"].stop()

            # Start both animations for them to be in sync
            self.player.animations["sprint"].start_animation()
            self.player.animations["sprint_side"].start_animation()
        elif game_controller.check_user_input(Input.DODGE) and self.player.cooldown_timers.dodge.has_seconds_passed(
                self.player.stats.dodge_cooldown):
            self.player.state = self.player.dodge_state_inst
        elif game_controller.is_moving():
            self.move(game_controller)
        else:
            self.player.state = self.player.idle_state_inst

    def move(self, game_controller: GameController) -> None:
        """
        Moves the player quickly
        :param game_controller: The Game Controller Instance
        """

        movement_input = game_controller.get_movement_vector()

        if movement_input.x != 0:

            if movement_input.x == -self.momentum_memory.x:
                self.momentum_timer.restart_time()

        if movement_input.y != 0:
            if movement_input.y == -self.momentum_memory.y:
                self.momentum_timer.restart_time()

        # Take max of that and 1 to prevent zero division error
        mag = math.sqrt(movement_input.x ** 2 + movement_input.y ** 2)
        mag = max(1.0, mag)

        self.player.position.x += self.player.stats.speed * movement_input.x / mag
        self.player.position.y += self.player.stats.speed * movement_input.y / mag

    def draw(self) -> None:
        """
        Changes the sprite for the character depending on the state
        """

        # Hide Idle Sprite
        self.player.game_obj["player"].sprite.visible = False

        if self.move_dir.x == 0 and abs(self.move_dir.y) == 1:
            dir_sprite = "walk"
            is_flipped = False
            self.player.animations["walk_side"].sprite.visible = False
        else:
            dir_sprite = "walk_side"
            is_flipped = self.move_dir.x != 1
            self.player.animations["walk"].sprite.visible = False

        self.player.animations[dir_sprite].run_repeating(is_flipped=is_flipped)
