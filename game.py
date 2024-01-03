"""
The Entry File for the Dungeon Crawler Game
By: Sean McClanahan
Last Modified: 12/31/2023
"""

import pygame

from Scripts.Engine.Engine import GameEngine

from Scripts.Camera.camera import Camera
from Scripts.Player.player import Player
from Scripts.UI.hud import HUD

if __name__ == "__main__":

    # Engine Setup
    engine = GameEngine()

    # Hide the mouse cursor
    pygame.mouse.set_visible(False)

    # Camera Setup
    cam = Camera()

    # Player Setup
    player_size = 50
    player_color = (0, 128, 255)
    player = Player(
        initial_position=pygame.Vector2(1000, 1000),
        camera=cam
    )
    player.sprite.move(
        engine.screen_width // 2 - player_size // 2,
        engine.screen_height // 2 - player_size // 2
    )
    player_hud = HUD(player)

    while engine.is_running():
        engine.screen.fill((0, 0, 0))

        # Get the state of all keys
        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        # Update the player based on the current state
        player.update(keys, mouse_buttons, mouse_pos)

        cam.center_player(player)
        cam.sorted_draw()

        player_hud.update()
        player_hud.draw(engine.screen)

        engine.tick()

    # Once the while loop is broken, quit
    engine.quit()
