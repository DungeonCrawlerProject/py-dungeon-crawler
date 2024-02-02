"""
The Animation class for animating PNGSprites
By: Sean McClanahan
Last Modified: 02/01/2024
"""

import pygame

from Scripts.sprite import PNGSprite


class Animation:

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

        self.sprite = sprite
        self.display_duration = display_duration
        self.start_time = None
        self.current_sprite_index = 0

    def start_animation(self) -> None:
        """
        Begins the animation timer and sets the frame to zero
        """
        self.start_time = pygame.time.get_ticks()
        self.current_sprite_index = 0

    def run(
            self,
            elapsed_time: float,
            is_replaying: bool = False
    ) -> int | None:
        """
        Runs the animation
        :param elapsed_time: The timer showing the time differential
        :param is_replaying: Whether the animation should replay
        :return: None represents the animation should not play. An int represents the frame index to animate
        """

        # Return if the timer has been started
        if self.start_time is None:
            return None

        # If the sprite is out of index return (this will be refactored when doing re-playable animations)
        if not is_replaying:

            # If exceeded the duration return
            if elapsed_time > self.display_duration:
                return None
            if self.current_sprite_index >= len(self.sprite.frames):
                return None

            if elapsed_time > (self.current_sprite_index + 1) * (self.display_duration // len(self.sprite.frames)):
                self.current_sprite_index += 1

            self.current_sprite_index %= len(self.sprite.frames)
            return self.current_sprite_index

        else:

            # Prevents zero division error
            if elapsed_time == 0:
                _ind = 0

            time_per_frame = self.display_duration // len(self.sprite.frames)
            self.current_sprite_index = int(elapsed_time // time_per_frame)

        # Return the index
        return self.current_sprite_index
