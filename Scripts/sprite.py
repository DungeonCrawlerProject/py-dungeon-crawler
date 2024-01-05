from typing import List

import pygame
from pygame.sprite import Sprite


class PNGSprite(Sprite):

    @classmethod
    def make_from_sprite_sheet(
            cls,
            group: Sprite,
            sprite_sheet: pygame.Surface,
            width: int,
            height: int,
    ):

        inst = cls(group=group)
        inst.frames = inst.chop_sprite(sprite_sheet, width, height)
        inst.image = inst.frames[0]
        return inst

    def __init__(
            self,
            group: Sprite
    ) -> None:

        super().__init__(group)

        self.frames = []
        self.image = None
        self.rect = None

    @staticmethod
    def chop_sprite(
            sprite_sheet: pygame.Surface,
            width: int,
            height: int
    ) -> List[pygame.Surface]:
        """
        Separates the sprite into a list of sprites based on the parameters
        :param sprite_sheet: The input sprite-sheet for the object
        :param width: The width of a single frame for the object
        :param height: The height of a single frame for the object
        :return: List of individual frames
        """

        _x, _y = sprite_sheet.get_size()

        lst_img = []
        for j in range(_y // height):

            for i in range(_x // 32):
                _sprite = sprite_sheet.subsurface(pygame.rect.Rect(i * width, j * height, width, height))
                lst_img.append(_sprite)

        return lst_img

    def move(
            self,
            x: float | int,
            y: float | int
    ):
        self.rect = self.image.get_rect(center=(x, y))
