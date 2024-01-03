from typing import Tuple

import pygame
from pygame.sprite import Sprite


class PNGSprite(Sprite):

    def __init__(
            self,
            group: Sprite
    ) -> None:
        """

        :param group:
        """

        super().__init__(group)

        self.image = pygame.image.load('Sprites/Player.png').convert_alpha()
        self.rect = None

    def move(
            self,
            x: float | int,
            y: float | int
    ):
        self.rect = self.image.get_rect(center=(x, y))
