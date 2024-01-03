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

        self.frames = [
            pygame.image.load('Sprites/idle.png').convert_alpha(),
            pygame.image.load('Sprites/walk.png').convert_alpha(),
            pygame.image.load('Sprites/sprint.png').convert_alpha(),
            pygame.image.load('Sprites/Ground.png').convert_alpha(),
        ]

        self.image = self.frames[0]

        self.rect = None

    def move(
            self,
            x: float | int,
            y: float | int
    ):
        self.rect = self.image.get_rect(center=(x, y))
