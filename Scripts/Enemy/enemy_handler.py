import pygame
from Scripts.Enemy.enemy import Enemy

class EnemyHandler:
    def __init__(self) -> None:
        self.active_enemys = []
        self.active_targets = []

    def update(self):
        for enemy in self.active_enemys:
            enemy.update(self.active_targets)

    def add_enemy(self, enemy: Enemy):
        self.active_enemys.append(enemy)

    def remove_enemy(self, enemy: Enemy):
        self.active_enemys.remove(enemy)

    def add_target(self, target):
        self.active_targets.append(target)

    def remove_target(self, target):
        self.active_targets.remove(target)