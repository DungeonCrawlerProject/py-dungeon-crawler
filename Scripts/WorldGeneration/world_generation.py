import pygame
from Scripts.GameObject.game_object import GameObject
from typing import List
import random
import json
from Scripts.sprite import PNGSprite
from collections import defaultdict

class PointOfInterest:
    def __init__(self, name: str):
        ...

class Biome:
    def __init__(self, name: str):
        self.name = name
        with open(f"GameData/Biomes/{name}.json", 'r') as file:
            biome_data = json.load(file)
        self.tile_set = biome_data["tile_set"]
        self.points_of_interest: List[PointOfInterest] = biome_data["points_of_interest"]
        self.environment_objects = biome_data["env_objs"]


class WorldGeneration:
    TILE_SIZE = 32

    def __init__(self):
        self.ground = self.make_background(50, 40)
        self.game_objects: List[GameObject] = []

        self.generate_biomes([Biome("forest"), Biome("planes")])

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
        return pygame.Surface(size=(width*WorldGeneration.TILE_SIZE, height*WorldGeneration.TILE_SIZE))
    
    def generate_biomes(self, active_biomes: List[Biome]):
        right_border = self.ground.get_rect().right
        bot_border = self.ground.get_rect().bottom
        tile_map = [([0]*(right_border//32)) for i in range(bot_border//32)]
        placed_tiles = defaultdict(list)
        print(len(tile_map[39]))
        for biome in active_biomes:
            _pos = (random.randrange(0, right_border//32), random.randrange(0, bot_border//32))
            while tile_map[_pos[1]][_pos[0]] != 0:
                _pos = (random.randrange(0, right_border//32), random.randrange(0, bot_border//32))
            image = pygame.image.load(biome.tile_set)
            self.ground.blit(image, tuple([WorldGeneration.TILE_SIZE * cord for cord in _pos]))
            placed_tiles[biome.name].append(_pos)
            tile_map[_pos[1]][_pos[0]] = biome.name

        for i in range((right_border//32)*(bot_border//32)-2):
            for biome in active_biomes:
                for tile_pos in placed_tiles[biome.name]:
                    zero_neighbors = self.get_zero_neighbor(tile_map=tile_map, position=tile_pos)
                    if len(zero_neighbors) == 0:
                        continue
                    rand_tile_pos = zero_neighbors[random.randrange(0,len(zero_neighbors))]
                    image = pygame.image.load(biome.tile_set)
                    self.ground.blit(image, tuple([WorldGeneration.TILE_SIZE * cord for cord in rand_tile_pos]))
                    placed_tiles[biome.name].append(rand_tile_pos)
                    tile_map[rand_tile_pos[1]][rand_tile_pos[0]] = biome.name

    def get_zero_neighbor(self, tile_map, position):
        out = []
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                if position[0]+j < 0:
                    continue
                if position[1]+i < 0:
                    continue
                if position[0]+j >= 50:
                    continue
                if position[1]+i >= 40:
                    continue
                if tile_map[position[1]+i][position[0]+j] == 0:
                    out.append((position[0]+j, position[1]+i))
        return out