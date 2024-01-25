import pygame
from Scripts.Engine.engine import GameEngine
from Scripts.UI.button import Button


class EscMenu:
    def __init__(self, engine: GameEngine):
        self.engine = engine
        self.background = pygame.image.load('Sprites/EscMenu/EscMenuBackround.png')
        scalar = self.engine.screen_width/self.engine.min_window_width
        self.scaled_background = pygame.transform.scale_by(self.background, scalar)
        self.width = self.scaled_background.get_rect().width
        self.height = self.scaled_background.get_rect().height
        self.x = engine.screen_width * 0.30
        self.y = (engine.screen_height - self.height) / 2
        self.fit_buttons()
        self.in_menu = False

    def update(self, keys, mouse_buttons, mouse_pos):
        if not self.in_menu and keys[pygame.K_ESCAPE]:
            self.in_menu = True
        elif self.in_menu and keys[pygame.K_ESCAPE]:
            self.in_menu = False

        if not self.in_menu:
            return

        for button in self.buttons:
            if mouse_pos[0] < button.x or mouse_pos[0] > button.x + button.width:
                continue
            if mouse_pos[1] < button.y or mouse_pos[1] > button.y + button.height:
                continue
            if mouse_buttons[0]:
                button.click()

        scalar = self.engine.screen_width/self.engine.min_window_width
        self.scaled_background = pygame.transform.scale_by(self.background, scalar)
        self.width = self.scaled_background.get_rect().width
        self.height = self.scaled_background.get_rect().height
        self.x = self.engine.screen_width * 0.30
        self.y = (self.engine.screen_height - self.height) / 2
        self.fit_buttons()

    def draw(self, screen: pygame.Surface):
        if self.in_menu:
            screen_center = screen.get_rect().center
            background_center = self.scaled_background.get_rect().center
            pos = tuple(map(lambda x, y: x - y, screen_center, background_center))
            print(pos)
            screen.blit(self.scaled_background, pos)
            for button in self.buttons:
                button.draw(screen)

    def fit_buttons(self):
        self.buttons = []
        button_width = self.width * 0.7
        button_height = self.height * 0.1
        num_buttons = 4
        spacer = (self.height - (num_buttons * button_height)) / (num_buttons + 1)
        y = self.y + spacer
        resume = Button(
            x=self.x + self.width * .15,
            y=y,
            width=button_width,
            height=button_height,
            func=self.resume,
        )
        y += button_height + spacer
        settings = Button(
            x=self.x + self.width * 0.15,
            y=y,
            width=button_width,
            height=button_height,
            func=self.open_settings,
        )
        y += button_height + spacer
        quit_menu = Button(
            x=self.x + self.width * 0.15,
            y=y,
            width=button_width,
            height=button_height,
            func=self.quit_to_menu,
        )
        y += button_height + spacer
        quit_game = Button(
            x=self.x + self.width * 0.15,
            y=y,
            width=button_width,
            height=button_height,
            func=self.quit_game,
        )
        self.buttons.append(resume)
        self.buttons.append(settings)
        self.buttons.append(quit_menu)
        self.buttons.append(quit_game)

    def resume(self):
        self.in_menu = False

    def open_settings(self):
        print("settings")

    def quit_to_menu(self):
        print("quit to menu")

    def quit_game(self):
        self.engine.quit()
