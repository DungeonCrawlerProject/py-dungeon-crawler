import pygame
from Scripts.GameObject.game_object import GameObject
from typing import List
import random
from Scripts.sprite import PNGSprite

class WorldGeneration:
    def __init__(self):
        self.ground = self.make_background(100, 60)
        self.game_objects: List[GameObject] = []

        for i in range(100):
            _pos = (random.randrange(0, self.ground.get_rect().right), random.randrange(0, self.ground.get_rect().bottom))
            sprite_sheet = pygame.image.load('Sprites/Tree.png').convert_alpha()
            sprite = PNGSprite().make_from_sprite_sheet(sprite_sheet, 20, 40)
            self.game_objects.append(GameObject(_pos, sprite))

    #TODO
    # 1. make tile based background
    # 2. subdivide background into biomes
    # 3. place buildings and poi's in there corresponding biomes
    # 4. place crossroad nodes inside a box defined by the poi's
    # 5. build path network from tree made out of crossroads and poi's
    # 6. place environment filler based on density's defined by biome
            
    def make_background(self, width: int, height: int) -> pygame.Surface :
        TILE_SIZE = 32
        return pygame.Surface(size=(width*TILE_SIZE, height*TILE_SIZE))