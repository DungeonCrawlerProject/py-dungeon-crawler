import pygame
import json
import random
from typing import List
from Scripts.Enemy.enemy_loader import EnemyLoader
from Scripts.Enemy.enemy_handler import EnemyHandler
from Scripts.CollisionBox.collision_handler import CollisionHandler

from pydantic import BaseModel


class PointOfInterest(BaseModel):
    name: str
    sprite_sheet: str
    size: List[int]
    enemys: List[list]

    @classmethod
    def from_json(cls, path):
        with open(path, "r") as file:
            biome_data = json.load(file)
        inst = cls(**biome_data)

        return inst
    
    def spawn_enemys(self, pos, enemy_handler: EnemyHandler, collision_handler: CollisionHandler):
        for enemy_data in self.enemys:
            enemy_name = enemy_data[0]
            enemy_count = enemy_data[1]
            for _ in range(enemy_count):
                pos = pos + pygame.Vector2(random.randrange(-20, 20), random.randrange(-20, 20))
                enemy = EnemyLoader.load_from_json(enemy_name=enemy_name, pos=pos, collision_handler=collision_handler)
                enemy_handler.add_enemy(enemy=enemy)