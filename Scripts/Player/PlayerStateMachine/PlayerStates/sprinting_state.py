"""
Sprint State
By: Sean McClanahan
Last Modified: 02/03/2024
"""

import math

from pygame import Vector2

from Scripts.Player.PlayerStateMachine.player_state import IPlayerState
from Scripts.Utility.game_controller import GameController
from Scripts.Utility.input import Input


class SprintingState(IPlayerState):
    move_dir = Vector2(0, 0)

    def update(self, game_controller: GameController) -> None:
        """
        Updates the players state, includes player movement and state switching
        :param game_controller: The Game Controller Instance
        """

        self.move_dir = game_controller.get_movement_vector()

        if not game_controller.is_moving():
            self.player.animations["sprint"].stop()
            self.player.animations["sprint_side"].stop()

        if not game_controller.is_moving():
            self.player.state = self.player.idle_state_inst
        elif game_controller.check_user_input(Input.DODGE) and self.player.cooldown_timers.dodge.has_seconds_passed(self.player.stats.dodge_cooldown):
            self.player.state = self.player.dodge_state_inst
        else:
            self.move(game_controller)

    def move(self, game_controller: GameController) -> None:
        """
        Moves the player quickly
        :param game_controller: The Game Controller Instance
        """

        # Create an instance of GameControls
        movement_input = game_controller.get_movement_vector()

        # Take max of that and 1 to prevent zero division error
        mag = math.sqrt(movement_input.x ** 2 + movement_input.y ** 2)
        mag = max(1.0, mag)

        self.player.position.x += self.player.stats.speed * movement_input.x * self.player.stats.sprint_factor / mag
        self.player.position.y += self.player.stats.speed * movement_input.y * self.player.stats.sprint_factor / mag

    def draw(self):
        """
        Changes the sprite for the character depending on the state
        """

        # Hide Idle Sprite
        self.player.game_obj["player"].sprite.visible = False

        if self.move_dir.x == 0 and abs(self.move_dir.y) == 1:
            dir_sprite = "sprint"
            is_flipped = False
            self.player.animations["sprint_side"].sprite.visible = False
        else:
            dir_sprite = "sprint_side"
            is_flipped = self.move_dir.x != 1
            self.player.animations["sprint"].sprite.visible = False

        self.player.animations[dir_sprite].run_repeating(is_flipped=is_flipped)
