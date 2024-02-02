from dataclasses import dataclass

import pygame
from Scripts.sprite import PNGSprite
from typing import Optional, Tuple
from Scripts.CollisionBox.collision_box import CollisionBox


@dataclass
class GameObject:

    #: The position of the game object
    position: pygame.Vector2 | Tuple[float | int, float | int]

    #: The sprite for rendering the game object
    sprite: PNGSprite | pygame.Surface | None

    #: The collision box for the game object
    collider: Optional[CollisionBox] = None

    #: The amount of time that the object will exist for after instantiation measured in milliseconds
    lifetime: Optional[int] = None
    spawn_time: Optional[int] = None

    #: The type of game object
    tag: Optional[str] = None