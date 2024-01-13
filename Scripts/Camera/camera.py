"""
The Camera Class
By: Nick Petruccelli
Last Modified: 01/04/2023
"""

from typing import List

import pygame

from Scripts.GameObject.game_object import GameObject
from Scripts.Player.player import Player


class Camera(pygame.sprite.Group):

    def __init__(self, world):
        """
        The Camera class chases the player and renders the game objects
        """

        super().__init__()

        self.position = None

        self.display_surface = pygame.display.get_surface()

        _x, _y = self.display_surface.get_size()
        self.center = pygame.Vector2(_x // 2, _y // 2)

        self.ground_surf = world.ground
        self.ground_rect = self.ground_surf.get_rect(topleft=(0, 0))
        self.offset = pygame.Vector2(0, 0)
        self.game_objects = world.game_objects 

    def center_player(
            self,
            player: Player,
            strength: float = 1.0
    ) -> None:
        """
        Moves the camera towards the player's center
        :param player: The player instance
        :param strength: The speed at which the camera should follow the player
        """

        self.offset = strength * (player.position - self.position)
        self.position += self.offset

        if self.position[0] - self.center[0] < 0:
            self.position[0] = 0 + self.center[0]
        if self.position[1] - self.center[1] < 0:
            self.position[1] = 0 + self.center[1]
        if self.position[0] + self.center[0] > self.ground_rect.right:
            self.position[0] = self.ground_rect.right - self.center[0]
        if self.position[1] + self.center[1] > self.ground_rect.bottom:
            self.position[1] = self.ground_rect.bottom - self.center[1]
 
    def sorted_draw(self) -> None:
        """
        Renders the game scene
        """

        # Ground
        ground_offset = self.center - self.position

        # Draws the ground first
        self.display_surface.blit(self.ground_surf, ground_offset)

        # Env Player and Enemies
        for game_object in sorted(self.game_objects, key= lambda game_object: game_object.position[1]):
            sprite_offset = game_object.position + ground_offset

            # Draws the player last
            self.display_surface.blit(game_object.sprite.image, sprite_offset)
