import pygame
from Scripts.sprite import PNGSprite

class GameObject():
    def __init__(self, position: pygame.Vector2, sprite: PNGSprite) -> None:
        self.position = position
        self.sprite = sprite