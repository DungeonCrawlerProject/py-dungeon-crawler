from dataclasses import dataclass

import pygame
from Scripts.sprite import PNGSprite


@dataclass
class GameObject:

    #: The position of the game object
    position: pygame.Vector2

    #: The sprite for rendering the game object
    sprite: PNGSprite
