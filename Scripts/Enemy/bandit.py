import pygame
import json
from Scripts.Enemy.enemy import Enemy
from Scripts.sprite import PNGSprite


class Bandit(Enemy):
    def __init__(
        self,
        position: pygame.Vector2,
        sprite: PNGSprite,
        max_health: int,
        speed: float,
        attack_damage: int,
        attack_range: int,
        aggro_range: int
    ) -> None:
        super().__init__(
            position=position,
            sprite=sprite,
            max_health=max_health,
            speed=speed,
            attack_damage=attack_damage,
            attack_range=attack_range,
            aggro_range=aggro_range
        )

    @classmethod
    def load_from_json(cls, data_path, pos):
        with open(data_path, "r") as file:
            data = json.load(file)
            sprite = data["sprite"]
            max_health = data["max_health"]
            speed = data["speed"]
            attack_damage = data["attack_damage"]
            attack_range = data["attack_range"]
            aggro_range = data["aggro_range"]

        sprite = PNGSprite.make_single_sprite(sprite)
        enemy = Bandit(
            position=pos,
            sprite=sprite,
            max_health=max_health,
            speed=speed,
            attack_damage=attack_damage,
            attack_range=attack_range,
            aggro_range=aggro_range,
        )
        return enemy

    def move(self):
        print("move")
        if self.target is None:
            return
        self_to_target = self.target.position - self.position
        move_dir = self_to_target.normalize()
        if self_to_target.length() > self.attack_range:
            self.position += move_dir * self.speed


    def attack(self):
        if self.target is None:
            return
        dist_to_target = (self.target.position - self.position).length()
        if dist_to_target < self.attack_range:
            print("attack")
        
