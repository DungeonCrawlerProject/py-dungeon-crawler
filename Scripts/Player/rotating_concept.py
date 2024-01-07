import pygame
import sys
import math

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Load the image
image = pygame.image.load("Sprites/sprite_sheet.png").convert_alpha()
image_rect = image.get_rect()

image_center = [screen_width // 2, screen_height // 2]
image_angle = 0
image_rotation_speed = 10

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mouse_x, mouse_y = pygame.mouse.get_pos()

    dx = mouse_x - image_center[0]
    dy = mouse_y - image_center[1]
    target_angle = (math.degrees(math.atan2(dx, dy)) + 360) % 360

    image_angle += image_rotation_speed * math.sin(math.radians(target_angle - image_angle))

    rotated_image = pygame.Surface(image_rect.size, pygame.SRCALPHA)
    rotated_image = pygame.transform.rotate(image, image_angle)
    rotated_image_rect = rotated_image.get_rect(center=image_center)

    screen.fill((255, 255, 255))
    screen.blit(rotated_image, rotated_image_rect.topleft)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
