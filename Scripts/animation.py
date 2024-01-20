import pygame
import sys


class Animation:

    def __init__(self, screen_inst, transition_duration):
        self.screen = screen_inst  # TODO IN REAL CLASS THIS IS NOT NEEDED
        self.rect = pygame.Rect(300, 200, 200, 200)  # TODO IN REAL CLASS THIS IS NOT NEEDED
        self.transition_duration = transition_duration
        self.frames = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
        self.start_time = None

    def start_animation(self):
        self.start_time = pygame.time.get_ticks()

    def run(self):
        if self.start_time is not None:
            elapsed_time = pygame.time.get_ticks() - self.start_time
            if elapsed_time <= self.transition_duration:
                color_index = (elapsed_time // (self.transition_duration // 3)) % 3
                current_color = self.frames[color_index]
            else:
                current_color = (255, 255, 255)  # Set the final color to white after transition

            # Fill the screen with white background
            self.screen.fill((255, 255, 255))

            # Draw the box with the current color
            pygame.draw.rect(self.screen, current_color, self.rect)

            return current_color
        return None


# THE FOLLOWING IS NOT NEEDED FOR CLASS
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
screen.fill((255, 255, 255))

# Create an instance of ColoredBox with a specified transition duration
colored_box = Animation(screen, 1000)

# THE FOLLOWING IS NOT NEEDED FOR CLASS
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # THIS IS LIKE THE EVENT HANDLER
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # THIS IS SPUN UP IN THE PLAYER CLASS
            colored_box.start_animation()

    # This can be done in player draw
    colored_box.run()

    # THE FOLLOWING IS NOT NEEDED FOR CLASS
    pygame.display.flip()
    clock.tick(60)
