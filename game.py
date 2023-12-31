"""
The Entry File for the Dungeon Crawler Game
By: Sean McClanahan
Last Modified: 12/26/2023
"""

import math

import pygame

from Scripts.Engine.Engine import GameEngine
from Scripts.Player.player import Position, Player

if __name__ == "__main__":
    # Engine Setup
    engine = GameEngine()

    # Player Setup
    player_size = 50
    player_color = (0, 128, 255)
    player = Player()
    player.position = Position(
        engine.screen_width // 2 - player_size // 2,
        engine.screen_height // 2 - player_size // 2
    )

    # Loop
    while engine.is_running():

        # Get the state of all keys
        keys = pygame.key.get_pressed()

        # Update the player based on the current state
        player.update(keys)

        # Keep player within the engine.screen boundaries
        player.position.x = max(0, int(min(player.position.x, engine.screen_width - player_size)))
        player.position.y = max(0, int(min(player.position.y, engine.screen_height - player_size)))

        # Draw the backdrop
        engine.screen.fill((255, 255, 255))

        player.draw(screen=engine.screen)

        # Draw the players line of direction
        pygame.draw.line(
            surface=engine.screen,
            color=(0, 0, 0),
            start_pos=(player.position.x + player_size / 2, player.position.y + player_size / 2),
            end_pos=(
                math.cos(math.radians(player.angle)) * 100 + player.position.x + player_size / 2,
                math.sin(math.radians(player.angle)) * 100 + player.position.y + player_size / 2
            ),
            width=10
        )

        engine.tick()

    # Once the while loop is broken, quit
    engine.quit()
