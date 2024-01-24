import pygame

class Button:
    def __init__(self, x, y, width, height, func) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.func = func
    
    def draw(self, screen) -> None:
        pygame.draw.rect(screen, (211, 211, 211), (self.x, self.y, self.width, self. height))