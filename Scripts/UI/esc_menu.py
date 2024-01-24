import pygame
from Scripts.Engine.engine import GameEngine
from Scripts.UI.button import Button

class EscMenu():
    def __init__(self, engine: GameEngine):
        self.engine = engine
        self.width = engine.screen_width * .40
        self.height = self.width * 1.3
        self.x = engine.screen_width * .30
        self.y = (engine.screen_height - self.height)/2
        self.buttons = [Button(x=self.x+self.width*.05, y=self.y+self.height*.05, width=self.width*.9, height=self.height*.15, func=self.temp())]
        self.in_menu = False

    def update(self, keys):
        if not self.in_menu and keys[pygame.K_ESCAPE]:
            self.in_menu = True
        elif self.in_menu and keys[pygame.K_ESCAPE]:
            self.in_menu = False
        self.engine = self.engine
        self.width = self.engine.screen_width * .40
        self.height = self.width * 1.3
        self.x = self.engine.screen_width * .30
        self.y = (self.engine.screen_height - self.height)/2
        self.buttons = [Button(x=self.x+self.width*.05, y=self.y+self.height*.05, width=self.width*.9, height=self.height*.15, func=self.temp())]

    def draw(self, screen):
        if self.in_menu:
            pygame.draw.rect(screen, (100, 100, 100), (self.x, self.y, self.width, self.height))
            for button in self.buttons:
                button.draw(screen)
    
    def temp(self):
        pass