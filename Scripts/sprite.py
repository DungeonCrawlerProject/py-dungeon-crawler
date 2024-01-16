from typing import List

import pygame
from pygame.sprite import Sprite


class PNGSprite(Sprite):

    @classmethod
    def make_from_sprite_sheet(
            cls,
            sprite_sheet: pygame.Surface,
            width: int,
            height: int,
    ):
        inst = cls()
        inst.frames = inst.chop_sprite(sprite_sheet, width, height)
        inst.original_image = inst.frames[0]
        inst.image = inst.original_image.copy()  # Make a copy of the original image
        inst.rect = inst.image.get_rect()
        return inst

    @classmethod
    def make_single_sprite(cls, location):

        img = pygame.image.load(location).convert_alpha()

        inst = cls()
        inst.frames = inst.chop_sprite(img, img.get_width(), img.get_height())
        inst.original_image = inst.frames[0]
        inst.image = inst.original_image.copy()  # Make a copy of the original image
        inst.rect = inst.image.get_rect()
        return inst

    def __init__(self) -> None:

        super().__init__()

        self.frames = []
        self.original_image = None  # Store the original image for rotation
        self.image = None
        self.rect = None
        self.visible = True
        self.anchor = []

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

            for i in range(_x // width):
                _sprite = sprite_sheet.subsurface(pygame.rect.Rect(i * width, j * height, width, height))
                lst_img.append(_sprite)

        return lst_img

    def move(
            self,
            x: float | int,
            y: float | int
    ):
        self.rect = self.image.get_rect(center=(x, y))

    def rotate(self, deg: float) -> None:
        self.image = pygame.transform.rotate(self.original_image, deg)
        self.rect = self.image.get_rect(center=self.rect.center)
