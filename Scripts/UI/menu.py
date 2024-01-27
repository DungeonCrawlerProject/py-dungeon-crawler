import pygame
from Scripts.Engine.engine import GameEngine
from Scripts.UI.button import Button
from Scripts.UI.menu_handler import MenuHandler

class Menu:
    def __init__(self, engine: GameEngine, menu_handler: MenuHandler):
        self.engine = engine
        self.menu_handler = menu_handler
        self.background = pygame.image.load("Sprites/EscMenu/EscMenuBackround.png")
        self.buttons = []
        self.size_menu()
        self.in_menu = False

    def update(self, esc_down, mouse_button_down, mouse_pos):
        if not self.in_menu and esc_down:
            self.in_menu = True
        elif self.in_menu and esc_down:
            self.in_menu = False

        if not self.in_menu:
            return

        for button in self.buttons:
            if mouse_pos[0] < button.x or mouse_pos[0] > button.x + button.width:
                continue
            if mouse_pos[1] < button.y or mouse_pos[1] > button.y + button.height:
                continue
            if mouse_button_down:
                button.click()
        
        self.size_menu()

    def draw(self, screen: pygame.Surface):
        if self.in_menu:
            screen_center = screen.get_rect().center
            background_center = self.scaled_background.get_rect().center
            pos = tuple(map(lambda x, y: x - y, screen_center, background_center))
            screen.blit(self.scaled_background, pos)
            for button in self.buttons:
                button.draw(screen)

    def size_menu(self):
        scalar = self.engine.screen_width / self.engine.min_window_width
        self.scaled_background = pygame.transform.scale_by(self.background, scalar)
        self.width = self.scaled_background.get_rect().width
        self.height = self.scaled_background.get_rect().height
        self.x = self.engine.screen_width * 0.30
        self.y = (self.engine.screen_height - self.height) / 2
        self.fit_buttons()

    def fit_buttons(self):
        button_width = self.width * 0.7
        button_height = self.height * 0.1
        num_buttons = 4
        padding = 16
        spacer = ((self.height - padding * 2) - (num_buttons * button_height)) / (num_buttons + 1)
        y = self.y + padding + spacer
        for button in self.buttons:
            button.x = self.x + self.width * 0.15
            button.y = y
            button.width = button_width
            button.height = button_height
            y += button_height + spacer