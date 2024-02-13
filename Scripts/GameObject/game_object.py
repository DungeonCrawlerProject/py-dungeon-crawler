import math
from dataclasses import dataclass

import pygame
from pygame import Vector2

from Scripts.sprite import PNGSprite
from typing import Optional, Tuple
from Scripts.CollisionBox.collision_box import CollisionBox
from Scripts.Animation.sprite_animation import SpriteAnimation


@dataclass
class GameObject:

    #: The position of the game object
    position: pygame.Vector2 | Tuple[float | int, float | int]

    #: The sprite for rendering the game object
    sprite: PNGSprite | pygame.Surface | SpriteAnimation | None

    #: The collision box for the game object
    collider: Optional[CollisionBox] = None

    #: The amount of time that the object will exist for after instantiation measured in milliseconds
    lifetime: Optional[int] = None
    spawn_time: Optional[int] = None

    #: The type of game object
    tag: Optional[str] = None

    def rotate_about_object_center(
            self,
            center_object,
            angle: float,
            offset: float
    ) -> None:
        """
        Updates the position and angle of a game object owned by the player
        :param center_object: The object in which this game object rotates about
        :param angle: The angle of the object in degrees
        :param offset: The distance between the objects center and the player's center
        """

        # Rotate the object first to prevent bouncy animation
        self.sprite.rotate(angle)

        # Get the offset for the object
        offset_vector = Vector2(
            offset * math.sin(math.radians(angle)),
            offset * math.cos(math.radians(angle)),
        )

        # Grab the half of the size of the player
        object_to_rotate_about_half_size = Vector2(
            center_object.sprite.image.get_width() // 2,
            center_object.sprite.image.get_height() // 2
        )

        # Grab half of the size of the object
        this_half_size = Vector2(
            self.sprite.image.get_width() // 2,
            self.sprite.image.get_height() // 2,
        )

        full_offset = object_to_rotate_about_half_size - this_half_size + offset_vector

        self.position = center_object.position + full_offset
