"""
The Status Bar Class
By: Sean McClanahan
Last Modified: 12/31/23
"""

from typing import Tuple

import pygame


class StatusBar:

    def __init__(
            self,
            x: int,
            y: int,
            width: int,
            height: int,
            color: Tuple[int, int, int]
    ) -> None:
        """
        Places a Status bar
        :param x: The x position on the screen
        :param y: The y position on the screen
        :param width: The width of the bar
        :param height: The height of the bar
        :param color: The filled in color of the bar
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.value = 100
        self.color = color

    def update(self, new_value: float | int) -> None:
        """
        Updates the bar's progress
        :param new_value: The percentage to fill the bar 100% = 100.0
        """

        # Ensure the new value is within the valid range [0, 100]
        self.value = max(0, min(new_value, 100))

    def draw(self, screen) -> None:
        """
        Updates the graphic for the status bar
        :param screen: The pymunk screen
        """

        # Draw the black background
        pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.width, self.height))

        # Calculate the width of the fill based on the percentage
        fill_width = int((self.value / 100) * self.width)

        # Draw the yellow fill
        pygame.draw.rect(screen, self.color, (self.x, self.y, fill_width, self.height))
