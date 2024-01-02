import math
import pygame
from typing import Tuple
from Scripts.Player.player import Player

class Camera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0]
        self.half_hight = self.display_surface.get_size()[1]
        self.ground_surf = pygame.image.load('Sprites/Ground.png').convert_alpha()
        self.ground_rect = self.ground_surf.get_rect(topleft=(0,0))
        self.offset = pygame.math.Vector2(0,0)

    def add_player(self, player: Player):
       self.add(player.player_sprite) 

    def center_player(self, player: Player):
        self.offset[0] = player.position.x - self.half_width
        self.offset[1] = player.position.y - self.half_hight

    def sorted_draw(self):
        # Ground
        ground_offset = self.ground_rect.topleft + self.offset
        self.display_surface.blit(self.ground_surf, ground_offset)

        # Env Player and Enemys
        for sprite in sorted(self.sprites(), key= lambda sprite: sprite.rect.bottom):
            sprite_offset = sprite.rect.topleft + self.offset
            self.display_surface.blit(sprite.image, sprite_offset)

    # This is included below for potential use for dampening the camera.
    @staticmethod
    def smooth_damp(current_position, target_position, current_velocity, damping_ratio, delta_time=0.1):
        # Calculate the angular frequency
        omega_n = math.sqrt(1.0 - damping_ratio ** 2)

        # Calculate the exponential decay factor
        exp_term = math.exp(-damping_ratio * omega_n * delta_time)

        # Calculate the under damped response
        c = 1.0 / omega_n
        underdamped_response = c * exp_term * math.sin(
            omega_n * delta_time + math.atan(damping_ratio / math.sqrt(1.0 - damping_ratio ** 2)))

        # Update the position and velocity
        new_position = target_position + (
                    current_position - target_position + c * current_velocity) * exp_term * math.cos(
            omega_n * delta_time) + underdamped_response
        new_velocity = -omega_n * exp_term * (
                    current_position - target_position) + exp_term * current_velocity + underdamped_response

        return new_position, new_velocity


