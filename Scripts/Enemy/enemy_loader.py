import json
import pygame
from Scripts.Enemy.bandit import Bandit

class EnemyLoader:
    @classmethod
    def load_from_json(cls, enemy_name: str, pos: pygame.Vector2):
        match enemy_name:
            case "bandit":
                enemy = Bandit.load_from_json(data_path="GameData/Enemys/bandit.json", pos=pos)
                return enemy
