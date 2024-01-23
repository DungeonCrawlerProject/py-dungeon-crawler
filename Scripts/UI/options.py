import pygame
from Scripts.Engine.Engine import GameEngine

class Options():
    def __init__(self, engine: GameEngine):
        self.width = engine.screen_width * .40
        self.height = self.width * 1.5
        self.x = engine.screen_width * .30
        self.y = (engine.screen_height - self.height)/2

    def draw(self, screen):
        pygame.draw.rect(screen, (10, 10, 10), (self.x, self.y, self.width, self.height))