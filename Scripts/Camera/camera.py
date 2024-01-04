import math
import pygame
from Scripts.Player.player import Player
from Scripts.sprite import PNGSprite
from Scripts.GameObject.game_object import GameObject

class Camera(pygame.sprite.Group):

    def __init__(self):

        super().__init__()
        self.position = pygame.math.Vector2(10.0,10.0)
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0]//2
        self.half_hight = self.display_surface.get_size()[1]//2
        self.ground_surf = pygame.image.load('Sprites/Ground.png').convert_alpha()
        self.ground_rect = self.ground_surf.get_rect(topleft=(0, 0))
        self.offset = pygame.Vector2(0, 0)
        self.game_objects = list()

    def smooth_func(self, input):
        return pow(input, 2)

    def center_player(self, player: Player, strength: float):
        self.offset = strength*(player.position - self.position)
        print("Player pos- ", player.position)
        print("Cam pos- ", self.position)
        print("Offset- ", self.offset)
        self.position += self.offset

    def sorted_draw(self):

        # Ground
        ground_offset = -(self.position - pygame.Vector2(self.half_width, self.half_hight))
        self.display_surface.blit(self.ground_surf, ground_offset)

        # Env Player and Enemys
        for game_object in self.game_objects:
            sprite_offset = game_object.position - ground_offset
            self.display_surface.blit(game_object.sprite.image, sprite_offset)       
