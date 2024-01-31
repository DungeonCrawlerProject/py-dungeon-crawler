import pygame
import json
from Scripts.Enemy.enemy import Enemy
from Scripts.sprite import PNGSprite
from Scripts.CollisionBox.collision_handler import CollisionHandler


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
        collision_handler
    ) -> None:
        """Basic enemy that will wait for a target to enter aggro range and then move towards them and preform a melee attack.

        Args:
            position (pygame.Vector2): The position of the enemy.
            sprite (PNGSprite): The sprite of the enemy.
            max_health (int): The max health that a particular enemy can have.
            speed (float): The speed at which the enemy will move.
            attack_damage (int): The amount of hearts that will be removed from the player if hit by the enemy.
            attack_range (int): The range of the enemy's attacks
            aggro_range (int): The distance from the enemy's target before it will begin combat with the target.
            collision_handler (CollisionHandler): The collision handler associated with the enemy.
        """
        super().__init__(
            position=position,
            sprite=sprite,
            max_health=max_health,
            speed=speed,
            attack_damage=attack_damage,
            attack_range=attack_range,
            aggro_range=aggro_range,
            collision_handler=collision_handler
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
        enemy = Bandit(
            position=pos,
            sprite=sprite,
            max_health=max_health,
            speed=speed,
            attack_damage=attack_damage,
            attack_range=attack_range,
            aggro_range=aggro_range,
            collision_handler=collision_handler
        )
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
            player_collisions = self.collider.check_collision(tag="player")
            print(player_collisions)
            
        
