import pygame
from Enemy.enemy import Enemy
from Scripts.CollisionBox.collision_handler import CollisionHandler
from Scripts.sprite import PNGSprite


class Skermisher(Enemy):
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
        super().__init__(
            position,
            sprite,
            max_health,
            speed,
            attack_damage,
            attack_range,
            attack_windup,
            attack_cooldown,
            aggro_range,
            collision_handler,
        )
        self.melee_dist = 15

    def move(self, enemys):
        if self.target is None:
            return
        enemy_avoidance_vector = self.calc_enemy_avoidance_vector(enemys)

        self_to_target = self.target.position - self.position
        if self_to_target > self.melee_dist:
            move_dir = enemy_avoidance_vector.normalize()
        else:
            move_dir = (self_to_target + enemy_avoidance_vector).normalize()
        if self_to_target.length() > self.attack_range:
            self.position += move_dir * self.speed

    def attack(self):
        if self.target is None:
            return
        if self.last_attack > pygame.time.get_ticks() - self.attack_cooldown:
            return
        
        dist_to_target = self.target.position - self.position
        if dist_to_target > self.melee_dist:
            # Ranged Attack
            pass
