from Scripts.Engine.engine import GameEngine
from Scripts.UI.button import Button
from Scripts.UI.menu import Menu
from Scripts.UI.settings_menu import SettingsMenu


class EscMenu(Menu):
    def __init__(self, engine: GameEngine, settings_menu: SettingsMenu):
        super().__init__(engine)
        self.add_buttons()
        self.settings_menu = settings_menu

    def add_buttons(self):
        self.buttons = []
        button_width = self.width * 0.7
        button_height = self.height * 0.1
        num_buttons = 4
        padding = 16
        spacer = ((self.height - padding * 2) - (num_buttons * button_height)) / (num_buttons + 1)
        y = self.y + padding + spacer
        resume = Button(
            text="RESUME",
            x=self.x + self.width * .15,
            y=y,
            width=button_width,
            height=button_height,
            func=self.resume
        )
        y += button_height + spacer
        settings = Button(
            text="SETTINGS",
            x=self.x + self.width * 0.15,
            y=y,
            width=button_width,
            height=button_height,
            func=self.open_settings
        )
        y += button_height + spacer
        quit_menu = Button(
            text="QUIT TO MENU",
            x=self.x + self.width * 0.15,
            y=y,
            width=button_width,
            height=button_height,
            func=self.quit_to_menu
        )
        y += button_height + spacer
        quit_game = Button(
            text="QUIT GAME",
            x=self.x + self.width * 0.15,
            y=y,
            width=button_width,
            height=button_height,
            func=self.quit_game
        )
        self.buttons.append(resume)
        self.buttons.append(settings)
        self.buttons.append(quit_menu)
        self.buttons.append(quit_game)

    def resume(self):
        self.in_menu = False

    def open_settings(self):
        self.in_menu = False
        self.settings_menu.in_menu = True
        
    def quit_to_menu(self):
        print("quit to menu")

    def quit_game(self):
        self.engine.quit()
