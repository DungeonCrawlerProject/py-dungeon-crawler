from dataclasses import dataclass

import pygame
from Scripts.sprite import PNGSprite
from typing import Optional


@dataclass
class GameObject:

    #: The position of the game object
    position: pygame.Vector2

    #: The sprite for rendering the game object
    sprite: PNGSprite

    #: The type of gameobject
    tag: Optional[str] = None