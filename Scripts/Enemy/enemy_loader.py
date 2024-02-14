import json
import pygame
from Scripts.Enemy.bandit import Bandit
from Scripts.Enemy.skirmisher import Skirmisher
from Scripts.CollisionBox.collision_handler import CollisionHandler


class EnemyLoader:
    @classmethod
    def load_from_json(
        cls,
        enemy_name: str,
        pos: pygame.Vector2,
        collision_handler: CollisionHandler,
    ):
        match enemy_name:
            case "bandit":
                enemy = Bandit.load_from_json(
                    data_path="GameData/Enemys/bandit.json",
                    pos=pos,
                    collision_handler=collision_handler,
                )
                return enemy
            case "skirmisher":
                enemy = Skirmisher.load_from_json(
                    data_path="GameData/Enemys/skirmisher.json",
                    pos=pos,
                    collision_handler=collision_handler,
                )
                return enemy
