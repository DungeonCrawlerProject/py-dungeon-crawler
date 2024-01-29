import pygame
import json
from abc import ABC, abstractmethod
from Scripts.sprite import PNGSprite
from Scripts.GameObject.game_object import GameObject
from Scripts.CollisionBox.collision_box import CollisionBox

class Enemy(ABC, GameObject):
    def __init__(
        self,
        position: pygame.Vector2,
        sprite: PNGSprite,
        max_health: int,
        speed: float,
        attack_damage: int,
        attack_range: int,
        aggro_range: int,
        collider: CollisionBox
    ) -> None:
        super().__init__(position=position, sprite=sprite, tag="Enemy")
        self.max_health: int = max_health
        self.cur_health: int = max_health
        self.speed: float = speed
        self.attack_damage: int = attack_damage
        self.attack_range: int = attack_range
        self.aggro_range = aggro_range
        self.target = None
        self.collider = collider

    def idle(self, targets: list):
        for target in targets:
            target_distance = (target.position - self.position).length()
            if target_distance <= self.aggro_range:
                self.target = target
                break

    def update(self, targets):
        if self.target is None:
            self.idle(targets)
            return
        self.move()
        self.attack()

        dist_to_target = pygame.Vector2(self.target.position - self.position).length()
        if dist_to_target > self.aggro_range * 1.5:
            self.target = None

    @abstractmethod
    def move(self) -> None:
        """
        dictates how the enemy movement will work

        """
        pass

    @abstractmethod
    def attack(self):
        """
        dictates how the enemy will attack
        """
        pass
