"""
The Entry File for the Dungeon Crawler Game
By: Sean McClanahan
Last Modified: 01/27/2024
"""

import pygame

from Scripts.Utility.game_controller import GameController
from Scripts.Enemy.enemy import Enemy
from Scripts.Engine.engine import GameEngine

from Scripts.Camera.camera import Camera
from Scripts.Player.player import Player
from Scripts.UI.hud import HUD
from Scripts.WorldGeneration.world_generation import WorldGeneration
from Scripts.UI.menu_handler import MenuHandler
from Scripts.UI.esc_menu import EscMenu
from Scripts.UI.settings_menu import SettingsMenu
from Scripts.Enemy.enemy_handler import EnemyHandler
from Scripts.CollisionBox.collision_handler import CollisionHandler

if __name__ == "__main__":

    # Engine Setup
    engine = GameEngine()

    # Hide the mouse cursor
    # pygame.mouse.set_visible(False)

    enemy_handler = EnemyHandler()
    
    collision_handler = CollisionHandler()

    # World Gen
    world = WorldGeneration(enemy_handler, collision_handler)

    # Camera Setup
    cam = Camera(world)

    # UI Setup
    menu_handler = MenuHandler()
    esc_menu = EscMenu(engine, menu_handler)
    setting_menu = SettingsMenu(engine, menu_handler)
    menu_handler.set_menus(esc_menu=esc_menu, setting_menu=setting_menu)

    # Player Setup
    player_size = 50
    player_color = (0, 128, 255)
    ds = pygame.display.get_surface()
    init_x = ds.get_size()[0]//2
    init_y = ds.get_size()[1]//2
    player = Player(
        initial_position=pygame.Vector2(init_x, init_y),
        camera=cam,
        collision_handler=collision_handler
    )
    player.sprite.move(
        engine.screen_width // 2 - player_size // 2,
        engine.screen_height // 2 - player_size // 2
    )
    player_hud = HUD(player, engine)

    enemy_handler.add_target(target=player)

    # Initialize the first connected controller
    controller = None
    for i in range(pygame.joystick.get_count()):
        controller = pygame.joystick.Joystick(i)
        controller.init()
        break

    game_controller = GameController()

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
            if window_size[0] <= engine.min_window_width and window_size[1] <= engine.min_window_height:
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

        game_controller.update_inputs(keys, controller)

        # Update the player based on the current state
        player.update(game_controller, mouse_buttons, mouse_pos)

        #Update Enemys
        enemy_handler.update()

        cam.center_player(player, .1)
        cam.sorted_draw()

        menu_handler.update_current(esc_down, mouse_button_down, mouse_pos)
        menu_handler.draw_current(engine.screen)

        player_hud.update(esc_down, mouse_button_down, mouse_pos)
        player_hud.draw(engine.screen)

        engine.tick()

    # Once the while loop is broken, quit
    engine.quit()
