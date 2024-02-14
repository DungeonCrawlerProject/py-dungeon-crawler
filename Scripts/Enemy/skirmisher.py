import pygame
import math
import json
from Scripts.Enemy.enemy import Enemy
from Scripts.CollisionBox.collision_handler import CollisionHandler
from Scripts.sprite import PNGSprite
from Scripts.Animation.sprite_animation import SpriteAnimation
from Scripts.GameObject.game_object import GameObject
from Scripts.CollisionBox.collision_box import CollisionBox


class Skirmisher(Enemy):
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
        self.melee_dist = 60

    @classmethod
    def load_from_json(cls, data_path, pos, collision_handler):
        with open(data_path, "r") as file:
            data = json.load(file)
            sprite = data["sprite"]
            max_health = data["max_health"]
            speed = data["speed"]
            attack_damage = data["attack_damage"]
            attack_range = data["attack_range"]
            attack_windup = data["attack_windup"]
            attack_cooldown = data["attack_cooldown"]
            aggro_range = data["aggro_range"]

        sprite = PNGSprite.make_single_sprite(sprite)
        enemy = Skirmisher(
            position=pos,
            sprite=sprite,
            max_health=max_health,
            speed=speed,
            attack_damage=attack_damage,
            attack_range=attack_range,
            attack_windup=attack_windup,
            attack_cooldown=attack_cooldown,
            aggro_range=aggro_range,
            collision_handler=collision_handler,
        )
        return enemy

    def move(self, enemys):
        if self.target is None:
            return
        enemy_avoidance_vector = self.calc_enemy_avoidance_vector(enemys)

        self_to_target = self.target.position - self.position
        if self_to_target.length() > self.melee_dist:
            move_dir = enemy_avoidance_vector
            print("skir")
        else:
            move_dir = (self_to_target + enemy_avoidance_vector).normalize()
            print("melee")
        if self_to_target.length() > self.attack_range:
            self.position += move_dir * self.speed

    def attack(self):
        if self.target is None:
            return
        if self.last_attack > pygame.time.get_ticks() - self.attack_cooldown:
            return
        
        dist_to_target = (self.target.position - self.position).length()
        if dist_to_target > self.melee_dist:
            if self.attack_start is None:
                self.attack_windup = pygame.time.get_ticks()
                return
            if self.attack_windup > pygame.time.get_ticks() - self.attack_start:
                return
            self.attack_start = None

            self_to_target = self.target.position - self.position
            attack_angle = math.atan2(-self_to_target.y, self_to_target.x)
            x_offset = self.sprite.rect.width // 2
            y_offset = self.sprite.rect.height // 2
            offset_vector = pygame.Vector2(
                x_offset * math.cos(attack_angle),
                -y_offset * math.sin(attack_angle),
            )

            pos = self.position + 1.5 * offset_vector

            print(pos)


        else:
            if dist_to_target < self.attack_range or self.attack_start is not None:
                if self.attack_start is None:
                    self.attack_start = pygame.time.get_ticks()
                    return
                if self.attack_windup > pygame.time.get_ticks() - self.attack_start:
                    return
                self.attack_start = None
                attack_direction = (self.target.position) - (self.position)

                attack_angle = math.atan2(-attack_direction.y, attack_direction.x)
                x_offset = self.sprite.rect.width // 2
                y_offset = self.sprite.rect.height // 2
                offset_vector = pygame.Vector2(
                    x_offset * math.cos(attack_angle),
                    -y_offset * math.sin(attack_angle),
                )

                pos = self.position + 1.5 * offset_vector

                attack_anim = SpriteAnimation.make_from_sprite_sheet('Sprites/Enemys/Slash.png', 22, 15, 100)
                attack_anim.rotate(math.degrees(attack_angle))
                attack_anim.rotate_all_frames(math.degrees(attack_angle))
                attack_anim.start_anim(is_repeating=False)

                attack = GameObject(
                    position=pos,
                    sprite=attack_anim,
                    lifetime=300,
                    spawn_time=pygame.time.get_ticks(),
                    tag="anim"
                )
                attack_collider = CollisionBox(
                    parent=attack,
                    position=attack.position,
                    dimensions=pygame.Vector2(
                        attack_anim.rect.width,
                        attack_anim.rect.height,
                    ),
                    collision_handler=self.collision_handler,
                    tag="enemy_atk",
                )
                attack.collider = attack_collider
                
                self.camera.add_game_object(attack)
                targets_hit = attack.collider.check_collision(tag="player")
                for target in targets_hit:
                    target.stats.current_health -= self.attack_damage
                    #knockback_vector = attack_direction.normalize() * self.knockback
                    #target.position += knockback_vector

                self.last_attack = pygame.time.get_ticks()
