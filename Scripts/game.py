import math

import pygame
import sys

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
player_x = screen_width // 2 - player_size // 2
player_y = screen_height // 2 - player_size // 2
player_speed = 5

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
    if keys[pygame.K_w]:
        player_y -= player_speed
    if keys[pygame.K_s]:
        player_y += player_speed
    if keys[pygame.K_a]:
        player_x -= player_speed
    if keys[pygame.K_d]:
        player_x += player_speed

    # Keep player within the screen boundaries
    player_x = max(0, min(player_x, screen_width - player_size))
    player_y = max(0, min(player_y, screen_height - player_size))

    # Get the mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()

    dx = mouse_x - player_x
    dy = mouse_y - player_y

    # Print the cursor position
    # print(f"Cursor Position: ({dx}, {dy})")

    angle = math.atan2(mouse_y - (player_y + player_size // 2), mouse_x - (player_x + player_size // 2))
    player_angle = math.degrees(angle)


    print(player_angle)

    # Draw the player and cursor position on the screen
    screen.fill((255, 255, 255))
    # pygame.draw.polygon(screen, player_color, ())
    pygame.draw.rect(screen, player_color, (player_x, player_y, player_size, player_size))

    new_x = math.cos(angle) * 100 + player_x + player_size / 2
    new_y = math.sin(angle) * 100 + player_y + player_size / 2

    pygame.draw.line(screen, (255,0,0), (player_x + player_size / 2, player_y + player_size / 2), (new_x, new_y), 10)

    pygame.draw.circle(screen, (0, 255, 0), (mouse_x - 10, mouse_y - 10), 20)

    pygame.display.flip()
    clock.tick(30)  # Adjust the frame rate as needed

pygame.quit()
sys.exit()
