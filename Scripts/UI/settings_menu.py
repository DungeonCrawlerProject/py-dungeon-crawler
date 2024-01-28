import pygame
import ctypes
from Scripts.Engine.engine import GameEngine
from Scripts.UI.button import Button
from Scripts.UI.menu import Menu
from Scripts.UI.menu_handler import MenuHandler

class SettingsMenu(Menu):
    def __init__(self, engine: GameEngine, menu_handler: MenuHandler):
        super().__init__(engine, menu_handler)
        self.add_buttons()
        self.in_menu = True
        self.fullscreen = False
        self.resolution_scale = 1
        self.base_resolution = pygame.Vector2(480, 270)
        self.back_clicked = False
        scaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100
        self.rec_res = (ctypes.windll.user32.GetSystemMetrics(0) * scaleFactor,
                         ctypes.windll.user32.GetSystemMetrics(1) * scaleFactor)
        print(self.rec_res)

    def update(self, esc_down, mouse_button_down, mouse_pos):
        if not self.in_menu and self.back_clicked:
            self.in_menu = True
        elif self.in_menu and self.back_clicked:
            self.in_menu = False
        self.back_clicked = False

        if not self.in_menu:
            return

        for button in self.buttons:
            if mouse_pos[0] < button.x or mouse_pos[0] > button.x + button.width:
                button.txt_color = (0, 0, 0)
                continue
            if mouse_pos[1] < button.y or mouse_pos[1] > button.y + button.height:
                button.txt_color = (0, 0, 0)
                continue
            if button.txt_color[0] < 65:
                button.txt_color = tuple([x + 20 for x in button.txt_color])
            if mouse_button_down:
                button.click()
        
        self.size_menu()

    def add_buttons(self):
        self.buttons = []
        button_width = self.width * 0.7
        button_height = self.height * 0.1
        num_buttons = 3
        padding = 16
        spacer = ((self.height - padding * 2) - (num_buttons * button_height)) / (num_buttons + 1)
        y = self.y + padding + spacer
        self.fullscreen_btn = Button(
            text="WINDOW",
            x=self.x + self.width * .15,
            y=y,
            width=button_width,
            height=button_height,
            func=self.fullscreen_toggle
        )
        y = button_height + spacer
        self.resolution_btn = Button(
            text="RESOLUTION: 480x270",
            x=self.x + self.width * .15,
            y=y,
            width=button_width,
            height=button_height,
            func=self.resolution_cycle
        )
        y = button_height + spacer
        back_btn = Button(
            text="BACK",
            x=self.x + self.width * .15,
            y=y,
            width=button_width,
            height=button_height,
            func=self.go_back
        )
        self.buttons.append(self.fullscreen_btn)
        self.buttons.append(self.resolution_btn)
        self.buttons.append(back_btn)

    def fullscreen_toggle(self):
        if self.fullscreen:
            self.fullscreen = False
            self.fullscreen_btn.text = "WINDOW"
            self.resolution_scale = -1
            self.resolution_cycle()
            pygame.display.set_mode(self.base_resolution * self.resolution_scale)
        else:
            self.fullscreen = True
            self.fullscreen_btn.text = "FULLSCREEN"
            self.resolution_btn.text = "RESOLUTION: RECOMMENDED"
            self.resolution_scale = 0
            pygame.display.set_mode(self.rec_res, pygame.FULLSCREEN)
    
    def resolution_cycle(self):
        self.resolution_scale += 1
        if self.resolution_scale == 4:
            self.resolution_scale = 0
        if self.fullscreen:
            match self.resolution_scale:
                case 0:
                    pygame.display.set_mode(self.rec_res, pygame.FULLSCREEN)
                    self.resolution_btn.text = "RESOLUTION: RECOMMENDED"
                case 1:
                    pygame.display.set_mode((480, 270), pygame.FULLSCREEN)
                    self.resolution_btn.text = "RESOLUTION: 480x270"
                case 2:
                    pygame.display.set_mode((960, 540), pygame.FULLSCREEN)
                    self.resolution_btn.text = "RESOLUTION: 960x540"
                case 3:
                    pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
                    self.resolution_btn.text = "RESOLUTION: 1920x1080"
        else:
            match self.resolution_scale:
                case 0:
                    pygame.display.set_mode(self.rec_res)
                    self.resolution_btn.text = "RESOLUTION: RECOMMENDED"
                case 1:
                    pygame.display.set_mode((480, 270))
                    self.resolution_btn.text = "RESOLUTION: 480x270"
                case 2:
                    pygame.display.set_mode((960, 540))
                    self.resolution_btn.text = "RESOLUTION: 960x540"
                case 3:
                    pygame.display.set_mode((1920, 1080))
                    self.resolution_btn.text = "RESOLUTION: 1920x1080"
            if self.resolution_scale == 4:
                self.resolution_scale = 0

    def go_back(self):
        self.menu_handler.switch_menu(self.menu_handler.esc_menu)