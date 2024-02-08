import pygame
import json
from abc import ABC, abstractmethod
from Scripts.sprite import PNGSprite
from Scripts.GameObject.game_object import GameObject
from Scripts.CollisionBox.collision_handler import CollisionHandler
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
        attack_windup: int,
        attack_cooldown: int,
        aggro_range: int,
        collision_handler: CollisionHandler,
    ) -> None:
        """The abstract class in which all other enemy's will be based on.

        Args:
            position (pygame.Vector2): The position of the enemy.
            sprite (PNGSprite): The sprite of the enemy.
            max_health (int): The max health that a particular enemy can have.
            speed (float): The speed at which the enemy will move.
            attack_damage (int): The amount of hearts that will be removed from the player if hit by the enemy.
            attack_range (int): The range of the enemy's attacks
            attack_cooldown (int): The time it takes for the enemy to be able to attack after performing a attack. Measured in milliseconds
            aggro_range (int): The distance from the enemy's target before it will begin combat with the target.
            collision_handler (CollisionHandler): The collision handler associated with the enemy.
        """
        dimensions = pygame.Vector2(sprite.rect.width, sprite.rect.height)
        collider = CollisionBox(
            parent=self,
            position=position,
            dimensions=dimensions,
            collision_handler=collision_handler,
            tag="enemy",
        )
        super().__init__(position=position, sprite=sprite, collider=collider, tag="Enemy")
        self.max_health: int = max_health
        self.cur_health: int = max_health
        self.speed: float = speed
        self.attack_damage: int = attack_damage
        self.attack_range: int = attack_range
        self.attack_windup: int = attack_windup
        self.attack_start: int = None
        self.attack_cooldown = attack_cooldown
        self.last_attack = -attack_cooldown
        self.aggro_range = aggro_range
        self.target = None
        self.camera = None
        self.collision_handler = collision_handler

    def add_camera(self, camera):
        self.camera = camera

    def idle(self, targets: list):
        """The default state of an enemy before a target enters its aggro range.

        Args:
            targets (list): A list of all of the enemy's attackable game objects. ex: player
        """
        for target in targets:
            target_distance = (target.position - self.position).length()
            if target_distance <= self.aggro_range:
                self.target = target
                break

    def update(self, targets, enemys):
        """Tells the enemy what behaviors to preform each frame as well as update its collision box to that it stays on the enemy sprite.

        Args:
            targets (_type_): A list of all of the enemy's attackable game objects. ex: player
        """
        self.collider.x = self.position.x
        self.collider.y = self.position.y
        if self.target is None:
            self.idle(targets)
            return
        self.move(enemys)
        self.attack()
        if self.target.stats.current_health <= 0:
            if self.target in targets:
                targets.remove(self.target)
            self.target = None

        if self.target is None:
            return
        dist_to_target = pygame.Vector2(self.target.position - self.position).length()
        if dist_to_target > self.aggro_range * 1.5:
            self.target = None

    @abstractmethod
    def move(self, enemys) -> None:
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

    def calc_enemy_avoidance_vector(self, enemys) -> pygame.Vector2:
        enemy_avoidance_vector = pygame.Vector2(0, 0)
        near_by_enemys = 0
        for enemy in enemys:
            self_to_enemy = (self.position - enemy.position)
            if self_to_enemy.length() > 50:
                continue
            if self_to_enemy.length() == 0:
                self_to_enemy = pygame.Vector2(.1, .1)
            enemy_avoidance_vector += self_to_enemy * (20 / self_to_enemy.length())
            near_by_enemys += 1
        enemy_avoidance_vector /= near_by_enemys
        return enemy_avoidance_vector
