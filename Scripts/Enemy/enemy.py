import pygame

from Scripts.Player.Stats.player_stats import PlayerStats
from Scripts.sprite import PNGSprite


class Enemy:

    def __init__(self, initial_position: pygame.Vector2):

        # Positional Variables
        self.position = initial_position
        self.relative_position = initial_position

        # Dataclasses
        self.stats = PlayerStats()
        self.stats.speed = 3

        # Make the sprite in the center
        self.sprite = PNGSprite.make_from_sprite_sheet('Sprites/sprite_sheet.png', 32, 64)

        self.stalking = None

    def watch(self, item):
        self.stalking = item

    def update(self) -> None:
        """
        Updates the Enemy object
        """

        # Change player pos
        self.draw()

        if self.stalking:
            dp = self.stalking.position - self.position

            if 0 < dp.magnitude() < 500:
                self.position += dp.normalize() * self.stats.speed

    def take_damage(self, damage: float) -> None:
        """
        Deals damage to the enemy
        :param damage: The damage
        """

        self.stats.current_health -= damage

        if self.stats.current_health < 0:
            self.kill()

    def kill(self) -> None:
        raise NotImplementedError

    def draw(self) -> None:
        ...

    def set_relative_position(self, offset):

        self.relative_position = self.position + offset
