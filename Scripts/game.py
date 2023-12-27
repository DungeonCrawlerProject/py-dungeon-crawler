import math

import pygame
import sys

from Scripts.Player.player import Position, Player

# Initialize Pygame
pygame.init()

# Pygame Setup
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("WASD Movement and Cursor Position Example")

# Player Setup

player_size = 50
player_color = (0, 128, 255)


player_position = Position(screen_width // 2 - player_size // 2, screen_height // 2 - player_size // 2)
player = Player(player_position, speed=5)


FRAME_RATE = 30

# Example Pygame Game Loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get the state of all keys
    keys = pygame.key.get_pressed()

    # Update player position based on key input
    movement_input = Position(0, 0)

    # Update player position based on key input
    if keys[pygame.K_w]:
        movement_input.y = -1
    if keys[pygame.K_s]:
        movement_input.y = 1
    if keys[pygame.K_a]:
        movement_input.x = -1
    if keys[pygame.K_d]:
        movement_input.x = 1

    mag = math.sqrt(movement_input.x ** 2 + movement_input.y ** 2)
    if keys[pygame.K_LSHIFT]:
        print("hit")
        player.position.x += player.speed * movement_input.x * player.sprint_factor / mag
        player.position.y += player.speed * movement_input.y * player.sprint_factor / mag
    elif mag != 0:
        player.position.x += player.speed * movement_input.x / mag
        player.position.y += player.speed * movement_input.y / mag

    # Keep player within the screen boundaries
    player.position.x = max(0, min(player.position.x, screen_width - player_size))
    player.position.y = max(0, min(player.position.y, screen_height - player_size))

    # Get the mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()

    dx = mouse_x - player.position.x
    dy = mouse_y - player.position.y

    # Print the cursor position
    # print(f"Cursor Position: ({dx}, {dy})")

    angle = math.atan2(mouse_y - (player.position.y + player_size // 2), mouse_x - (player.position.x + player_size // 2))
    player_angle = math.degrees(angle)

    # Draw the player and cursor position on the screen
    screen.fill((255, 255, 255))

    # pygame.draw.polygon(screen, player_color, ())
    pygame.draw.rect(screen, player_color, (player.position.x, player.position.y, player_size, player_size))

    new_x = math.cos(angle) * 100 + player.position.x + player_size / 2
    new_y = math.sin(angle) * 100 + player.position.y + player_size / 2

    pygame.draw.line(screen, (255, 0, 0), (player.position.x + player_size / 2, player.position.y + player_size / 2), (new_x, new_y), 10)

    pygame.draw.circle(screen, (0, 255, 0), (mouse_x - 10, mouse_y - 10), 20)

    pygame.display.flip()
    clock.tick(FRAME_RATE)  # Adjust the frame rate as needed

pygame.quit()
sys.exit()

if __name__ == "__main__":
    ...
