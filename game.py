"""
The Entry File for the Dungeon Crawler Game
By: Sean McClanahan
Last Modified: 01/27/2024
"""

import pygame

from GameData.game_controls import GameControls
from Scripts.Enemy.enemy import Enemy
from Scripts.Engine.Engine import GameEngine

from Scripts.Camera.camera import Camera
from Scripts.Player.player import Player
from Scripts.UI.hud import HUD
from Scripts.WorldGeneration.world_generation import WorldGeneration

if __name__ == "__main__":

    # Engine Setup
    engine = GameEngine()

    # Hide the mouse cursor
    # pygame.mouse.set_visible(False)

    # World Gen
    world = WorldGeneration()

    # Camera Setup
    cam = Camera(world)

    # Player Setup
    player_size = 50
    player_color = (0, 128, 255)
    ds = pygame.display.get_surface()
    init_x = ds.get_size()[0]//2
    init_y = ds.get_size()[1]//2
    player = Player(
        initial_position=pygame.Vector2(init_x, init_y),
        camera=cam
    )
    player.sprite.move(
        engine.screen_width // 2 - player_size // 2,
        engine.screen_height // 2 - player_size // 2
    )
    player_hud = HUD(player)

    enemy = Enemy(initial_position=pygame.Vector2(100, 100))
    cam.game_objects.append(enemy)

    # TODO THIS IS A BAD PRACTICE
    player.known_enemies.append(enemy)

    # Initialize the first connected controller
    controller = None
    for i in range(pygame.joystick.get_count()):
        controller = pygame.joystick.Joystick(i)
        controller.init()
        break

    game_controller = GameControls()

    while engine.is_running():
        engine.screen.fill((0, 0, 0))

        # Get the state of all keys
        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        game_controller.update_inputs(keys, controller)
        # Update the player based on the current state
        player.update(game_controller, mouse_buttons, mouse_pos)
        enemy.watch(player)
        enemy.update()

        cam.center_player(player, .1)
        cam.sorted_draw()

        player_hud.update()
        player_hud.draw(engine.screen)

        engine.tick()

    # Once the while loop is broken, quit
    engine.quit()
