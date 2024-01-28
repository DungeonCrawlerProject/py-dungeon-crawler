import pygame
import sys


class GameEngine:

    FRAME_RATE = 30

    def __init__(self):

        # Initialize Pygame
        pygame.init()

        # Pygame Setup
        self.min_window_width = 480
        self.min_window_height = 270
        self.screen_width = 480
        self.screen_height = 270
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Dungeon Crawler Prototype")

        self.clock = pygame.time.Clock()

    def is_running(self):
        for _event in pygame.event.get():
            if _event.type == pygame.QUIT:
                return False
        return True

    def tick(self):
        self.clock.tick(self.FRAME_RATE)
        pygame.display.flip()

    def quit(self):
        pygame.quit()
        sys.exit()
