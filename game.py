"""
The Entry File for the Dungeon Crawler Game
By: Sean McClanahan
Last Modified: 12/31/2023
"""

import pygame

from Scripts.Engine.Engine import GameEngine
from Scripts.Player.player import Player
from Scripts.UI.hud import HUD

if __name__ == "__main__":

    # Engine Setup
    engine = GameEngine()

    # Hide the mouse cursor
    pygame.mouse.set_visible(False)

    # Player Setup
    player_size = 50
    player_color = (0, 128, 255)
    player = Player(
        initial_position=pygame.Vector2(
            engine.screen_width // 2 - player_size // 2,
            engine.screen_height // 2 - player_size // 2
        )
    )

    player_hud = HUD(player)

    # Create an enemy
    initial_enemy_position = (1000, 1000)

    while engine.is_running():

        # Get the state of all keys
        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        # Update the player based on the current state
        player.update(keys, mouse_buttons, mouse_pos)

        # Keep player within the engine.screen boundaries
        player.position.x = max(0, int(min(player.position.x, engine.screen_width - player_size)))
        player.position.y = max(0, int(min(player.position.y, engine.screen_height - player_size)))

        # Draw the backdrop
        engine.screen.fill((139, 69, 13))

        player_hud.update()
        player_hud.draw(engine.screen)

        player.draw(screen=engine.screen)

        engine.tick()

    # Once the while loop is broken, quit
    engine.quit()
