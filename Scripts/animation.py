"""
The Animation class for animating PNGSprites
By: Sean McClanahan
Last Modified: 02/03/2024
"""

import pygame
from pygame import Vector2
from pygame.time import get_ticks

from Scripts.GameObject.game_object import GameObject
from Scripts.sprite import PNGSprite


class Animation(GameObject):

    def __init__(
            self,
            display_duration: float,
            sprite: PNGSprite
    ) -> None:
        """
        Creates the animator object
        :param display_duration: The time in milliseconds that the animation should play
        :param sprite: The PNGSprite, with more than one frame
        """

        # Initial Index Checking
        if len(sprite.frames) <= 1:
            raise IndexError("The Input PNGSprite must have more than one frame to animate")

        # Inherits Position and Sprite
        super().__init__(Vector2(0, 0), sprite)

        self.display_duration = display_duration
        self.start_time = None
        self.current_sprite_index = 0

        # Turn off the animation by default
        self.sprite.visible = False

    def start_animation(self) -> None:
        """
        Begins the animation timer and sets the frame to zero
        """
        self.start_time = pygame.time.get_ticks()
        self.sprite.visible = True
        self.current_sprite_index = 0

    def run_repeating(
            self,
            is_flipped: bool = False,
    ) -> None:
        """
        Runs the animation
        :param is_flipped: Whether the image should be flipped
        """

        self.sprite.visible = True

        # Return if the timer has been started
        if self.start_time is None:
            return None

        elapsed_time = (get_ticks() - self.start_time) % self.display_duration
        time_per_frame = self.display_duration // len(self.sprite.frames)
        self.current_sprite_index = int(elapsed_time // time_per_frame)

        if self.current_sprite_index is None:
            return

        self.sprite.change_frame(self.current_sprite_index, is_flipped=is_flipped)

    def run_once(
        self,
        elapsed_time: float,
        is_flipped: bool = False
    ) -> None:
        """
        Runs the animation
        :param elapsed_time: The timer showing the time differential
        :param is_flipped: Whether the image should be flipped
        """

        self.sprite.visible = True

        # Return if the timer has been started
        if self.start_time is None:
            return None

        # If exceeded the duration return
        if elapsed_time > self.display_duration:
            self.stop()
            return None
        if self.current_sprite_index >= len(self.sprite.frames):
            return None

        if elapsed_time > (self.current_sprite_index + 1) * (self.display_duration // len(self.sprite.frames)):
            self.current_sprite_index += 1

        self.current_sprite_index %= len(self.sprite.frames)

        if self.current_sprite_index is None:
            return

        self.sprite.change_frame(self.current_sprite_index, is_flipped=is_flipped)

    def stop(self):
        self.sprite.visible = False
