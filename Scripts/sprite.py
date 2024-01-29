import math
from typing import List

import pygame
from pygame.sprite import Sprite


class PNGSprite(Sprite):

    @classmethod
    def make_from_sprite_sheet(
            cls,
            location: str,
            width: int,
            height: int,
    ):
        img = pygame.image.load(location).convert_alpha()

        inst = cls()
        inst.frames = inst.chop_sprite(img, width, height)
        inst.__original_frames = inst.chop_sprite(img, width, height)
        inst.__original_image = inst.frames[0]
        inst.__unrotated_image = inst.chop_sprite(img, width, height)
        inst.image = inst.__original_image.copy()  # Make a copy of the original image
        inst.rect = inst.image.get_rect()
        return inst

    @classmethod
    def make_single_sprite(cls, location):

        img = pygame.image.load(location).convert_alpha()

        inst = cls()
        inst.frames = inst.chop_sprite(img, img.get_width(), img.get_height())
        inst.__original_frames = inst.chop_sprite(img, img.get_width(), img.get_height())
        inst.__original_image = inst.frames[0]
        inst.__unrotated_image = inst.chop_sprite(img, img.get_width(), img.get_height())
        inst.image = inst.__original_image.copy()  # Make a copy of the original image
        inst.rect = inst.image.get_rect()
        return inst

    def __init__(self) -> None:

        super().__init__()

        self.frames = []
        self.__original_frames = []
        self.__original_image = None  # Store the original image for rotation
        self.__unrotated_image = None
        self.current_frame = 0
        self.image = None
        self.rect = None
        self.visible = True
        self.anchor = []
        self._animation_start_clock = math.inf

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

    def change_frame(self, image_index: int) -> None:

        self.image = self.frames[image_index]
        self.current_frame = image_index

    def get_original_image(self):
        return self.__original_image

    def get_original_frames(self):
        return self.__original_frames

    def scale_frames(self, scalar):

        for i, frame in enumerate(self.frames):
            size = self.get_original_image().get_rect()
            a = pygame.Vector2(size.width, size.height)
            self.frames[i] = pygame.transform.scale(frame, scalar * a)
            self.__unrotated_image[i] = pygame.transform.scale(frame, scalar * a)


    def move(
            self,
            x: float | int,
            y: float | int
    ):
        self.rect = self.image.get_rect(center=(x, y))

    def rotate(self, deg: float) -> None:
        # THE ORIGINAL IMAGE NEEDS A REWORK
        safe_ref = self.__unrotated_image[self.current_frame]
        self.image = pygame.transform.rotate(safe_ref, deg)
        self.rect = self.image.get_rect(center=self.rect.center)
