"""
Walking State
By: Sean McClanahan
Last Modified: 01/27/2024
"""

import math

from pygame import Vector2
from pygame.time import get_ticks

from Scripts.Utility.cronos_clock import CronosClock
from Scripts.Utility.input import Input
from Scripts.Utility.game_controller import GameController
from Scripts.Player.PlayerStateMachine.player_state import IPlayerState


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

        if self.momentum_timer.has_seconds_passed(3.0):
            self.player.state = self.player.sprinting_state_inst

            # Start both animations for them to be in sync
            self.player.animations["sprint"].start_animation()
            self.player.animations["sprint_side"].start_animation()
        elif game_controller.check_user_input(Input.DODGE) and self.player.cooldown_timers.dodge.has_seconds_passed(self.player.stats.dodge_cooldown):
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

        self.player.game_obj["player"].sprite.visible = False

        _elapsed_time = get_ticks() - self.player.animations["walk"].start_time

        self.player.game_obj["walk"].sprite.visible = False
        self.player.game_obj["walk_side"].sprite.visible = False

        if self.move_dir.x == 0 and abs(self.move_dir.y) == 1:
            self.player.game_obj["walk"].sprite.visible = True
            self.player.game_obj["walk_side"].sprite.visible = False

            ind = self.player.animations["walk"].run(
                _elapsed_time % self.player.animations["walk"].display_duration,
                is_replaying=True
            )

            self.player.game_obj["walk"].sprite.change_frame(ind)
        else:

            self.player.game_obj["walk"].sprite.visible = False
            self.player.game_obj["walk_side"].sprite.visible = True

            ind = self.player.animations["walk_side"].run(
                _elapsed_time % self.player.animations["walk"].display_duration,
                is_replaying=True
            )

            if self.move_dir.x == 1:
                self.player.game_obj["walk_side"].sprite.change_frame(ind)
            else:
                self.player.game_obj["walk_side"].sprite.change_frame(ind, is_flipped=True)
