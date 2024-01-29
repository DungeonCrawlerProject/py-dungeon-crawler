from dataclasses import dataclass

import pygame
from Scripts.sprite import PNGSprite
from typing import Optional, Tuple


@dataclass
class GameObject:

    #: The position of the game object
    position: pygame.Vector2 | Tuple[float | int, float | int]

    #: The sprite for rendering the game object
    sprite: PNGSprite | pygame.Surface | None

    #: The type of gameobject
    tag: Optional[str] = None