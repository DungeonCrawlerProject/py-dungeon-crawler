import pygame
import sys

from Scripts.sprite import PNGSprite


class Animation:

    def __init__(self, display_duration, sprite: PNGSprite):
        self.sprite = sprite
        self.display_duration = display_duration
        self.start_time = None
        self.current_sprite_index = 0

    def start_animation(self):
        self.start_time = pygame.time.get_ticks()
        self.current_sprite_index = 0

    def run(self, elapsed_time):
        if self.start_time is not None:
            if elapsed_time <= self.display_duration and self.current_sprite_index < len(self.sprite.frames):
                # Draw the current sprite at the same position
                current_frame = self.sprite.frames[self.current_sprite_index]

                # Check if it's time to switch to the next sprite
                if elapsed_time > (self.current_sprite_index + 1) * (self.display_duration // len(self.sprite.frames)):
                    self.current_sprite_index += 1

                return current_frame
        return None


# THE FOLLOWING IS NOT NEEDED FOR CLASS
pygame.init()
screen = pygame.display.set_mode((200, 200))
clock = pygame.time.Clock()
screen.fill((255, 255, 255))

# Define paths to PNG images (replace with your actual image paths)
sprite_sheet = PNGSprite.make_from_sprite_sheet("../Sprites/slash.png", 40, 120)

# Create an instance of Animation with a specified display duration and a list of sprite paths
colored_animation = Animation(500, sprite_sheet)

# THE FOLLOWING IS NOT NEEDED FOR CLASS
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # THIS IS LIKE THE EVENT HANDLER
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # THIS IS SPUN UP IN THE PLAYER CLASS
            colored_animation.start_animation()

    # Calculate elapsed time
    current_time = pygame.time.get_ticks()

    if colored_animation.start_time is not None:
        _elapsed_time = current_time - colored_animation.start_time
    else:
        _elapsed_time = 0

    # Fill the screen with white background
    screen.fill((255, 255, 255))

    # Run the animation and get the current frame
    render_frame = colored_animation.run(_elapsed_time)

    # Draw the current frame at the specified position
    if render_frame is not None:
        screen.blit(render_frame, sprite_sheet.rect)

    # THE FOLLOWING IS NOT NEEDED FOR CLASS
    pygame.display.flip()
    clock.tick(60)
