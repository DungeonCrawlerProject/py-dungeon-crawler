import pygame
from Scripts.GameObject.game_object import GameObject
from typing import List
import random
from Scripts.sprite import PNGSprite

class WorldGeneration:
    def __init__(self, camera):
        self.ground = pygame.image.load('Sprites/Ground.png').convert_alpha()
        self.environment_objects: List[GameObject] = []

        for i in range(100):
            _pos = (random.randrange(0, self.ground.get_rect().right), random.randrange(0, self.ground.get_rect().bottom))
            sprite_sheet = pygame.image.load('Sprites/Tree.png').convert_alpha()
            sprite = PNGSprite(camera).make_from_sprite_sheet(camera, sprite_sheet, 20, 40)
            self.environment_objects.append(GameObject(_pos, sprite))