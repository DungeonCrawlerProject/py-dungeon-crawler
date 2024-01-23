import pygame
from Scripts.Engine.engine import GameEngine

class Options():
    def __init__(self, engine: GameEngine):
        self.engine = engine
        self.width = engine.screen_width * .40
        self.height = self.width * 1.5
        self.x = engine.screen_width * .30
        self.y = (engine.screen_height - self.height)/2
        self.in_menu = False

    def update(self, keys):
        if not self.in_menu and keys[pygame.K_ESCAPE]:
            self.in_menu = True
            print("true")
        elif self.in_menu and keys[pygame.K_ESCAPE]:
            print("false")
            self.in_menu = False
        if self.in_menu:
            self.draw(self.engine.screen)

    def draw(self, screen):
        pygame.draw.rect(screen, (10, 10, 10), (self.x, self.y, self.width, self.height))