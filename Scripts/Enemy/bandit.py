import pygame
import json
from Scripts.Enemy.enemy import Enemy
from Scripts.sprite import PNGSprite
from Scripts.CollisionBox.collision_box import CollisionBox


class Bandit(Enemy):
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
        super().__init__(
            position=position,
            sprite=sprite,
            max_health=max_health,
            speed=speed,
            attack_damage=attack_damage,
            attack_range=attack_range,
            aggro_range=aggro_range,
            collider=collider
        )

    @classmethod
    def load_from_json(cls, data_path, pos, collision_handler):
        with open(data_path, "r") as file:
            data = json.load(file)
            sprite = data["sprite"]
            max_health = data["max_health"]
            speed = data["speed"]
            attack_damage = data["attack_damage"]
            attack_range = data["attack_range"]
            aggro_range = data["aggro_range"]

        sprite = PNGSprite.make_single_sprite(sprite)
        dimensions = (sprite.rect.width, sprite.rect.height)
        collider = CollisionBox(position=pos, dimensions=dimensions, collision_handler=collision_handler, tag="enemy")
        collision_handler.add_collider(collider)
        enemy = Bandit(
            position=pos,
            sprite=sprite,
            max_health=max_health,
            speed=speed,
            attack_damage=attack_damage,
            attack_range=attack_range,
            aggro_range=aggro_range,
            collider=collider
        )
        collider.add_parent(enemy)
        return enemy

    def move(self):
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
            collisions = self.collider.check_collision()
            for collision in collisions:
                if collision.tag == "player":
                    print("hit")
        
