"""
The Entry File for the Dungeon Crawler Game
By: Sean McClanahan
Last Modified: 12/26/2023
"""

import math

import pygame

from Scripts.Engine.Engine import GameEngine
from Scripts.Player.player import Position, Player
from Scripts.Camera.camera import Camera

if __name__ == "__main__":
    # Engine Setup
    engine = GameEngine()

    #Camera Setup
    cam = Camera()

    # Player Setup
    player = Player((0, 0), cam)
    player.position = Position(400, 300)

    # Loop
    while engine.is_running():
        player.update()

        cam.center_player(player)
        cam.sorted_draw()

        # Keep player within the engine.screen boundaries
        #player.position.x = max(0, int(min(player.position.x, engine.screen_width - player_size)))
        #player.position.y = max(0, int(min(player.position.y, engine.screen_height - player_size)))

        # Draw the backdrop
        #engine.screen.fill((255, 255, 255))

        # Draw the players line of direction
        '''
        pygame.draw.line(
            surface=engine.screen,
            color=(255, 0, 0),
            start_pos=(player.position.x + player_size / 2, player.position.y + player_size / 2),
            end_pos=(
                math.cos(math.radians(player.angle)) * 100 + player.position.x + player_size / 2,
                math.sin(math.radians(player.angle)) * 100 + player.position.y + player_size / 2
            ),
            width=10
        )
'''
        engine.tick()

    # Once the while loop is broken, quit
    engine.quit()
