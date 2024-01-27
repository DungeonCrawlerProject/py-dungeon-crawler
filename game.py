"""
The Entry File for the Dungeon Crawler Game
By: Sean McClanahan
Last Modified: 12/31/2023
"""

import pygame

from Scripts.Enemy.enemy import Enemy
from Scripts.Engine.engine import GameEngine

from Scripts.Camera.camera import Camera
from Scripts.Player.player import Player
from Scripts.UI.hud import HUD
from Scripts.WorldGeneration.world_generation import WorldGeneration

if __name__ == "__main__":

    # Engine Setup
    engine = GameEngine()

    # Hide the mouse cursor
    # pygame.mouse.set_visible(False)

    #World Gen
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
    player_hud = HUD(player, engine)

    enemy = Enemy(initial_position=pygame.Vector2(100, 100))
    cam.game_objects.append(enemy)

    # TODO THIS IS A BAD PRACTICE
    player.known_enemies.append(enemy)

    is_running = True
    while is_running:
        engine.screen.fill((0, 0, 0))

        window_size = pygame.display.get_window_size()
        if window_size != (engine.screen_width, engine.screen_height):
            if window_size[0] > engine.min_window_width:
                scalar = window_size[0]/engine.min_window_width
                cam.rescale(scalar)
                engine.screen_width = window_size[0]
                engine.screen_height = window_size[1]
            if window_size[0] < engine.min_window_width and window_size[1] < engine.min_window_height:
                scalar = 1
                cam.rescale(scalar)
                engine.screen_width = engine.min_window_width
                engine.screen_height = engine.min_window_height
                engine.screen = pygame.display.set_mode((engine.min_window_width, engine.min_window_height), pygame.RESIZABLE)

        # Event Handling
        esc_down = False
        mouse_button_down = False
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.dict['key'] == pygame.K_ESCAPE:
                esc_down = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_button_down = True
            if event.type == pygame.QUIT:
                is_running = False
        # Get the state of all keys
        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        # Update the player based on the current state
        player.update(keys, mouse_buttons, mouse_pos)
        enemy.watch(player)
        enemy.update()

        cam.center_player(player, .1)
        cam.sorted_draw()

        player_hud.update(esc_down, mouse_button_down, mouse_pos)
        player_hud.draw(engine.screen)

        engine.tick()

    # Once the while loop is broken, quit
    engine.quit()
