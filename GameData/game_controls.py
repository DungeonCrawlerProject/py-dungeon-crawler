"""
The GameControl Handler
By: Sean McClanahan
Last Modified: 01/22/2024
"""

import pygame
import configparser


class GameControls:

    def __init__(
            self,
            config_file_path='GameData/controls.ini'
    ) -> None:
        """
        Initializes the GameControls object
        :param config_file_path: The relative path from the game.py file
        """

        self.CONTROLLER_DEAD_ZONE = 0.15

        # Define Pygame key constants for keyboard
        self.pygame_key_mapping_keyboard = {
            'A': pygame.K_a,
            'B': pygame.K_b,
            'C': pygame.K_c,
            'D': pygame.K_d,
            'E': pygame.K_e,
            'F': pygame.K_f,
            'G': pygame.K_g,
            'H': pygame.K_h,
            'I': pygame.K_i,
            'J': pygame.K_j,
            'K': pygame.K_k,
            'L': pygame.K_l,
            'M': pygame.K_m,
            'N': pygame.K_n,
            'O': pygame.K_o,
            'P': pygame.K_p,
            'Q': pygame.K_q,
            'R': pygame.K_r,
            'S': pygame.K_s,
            'T': pygame.K_t,
            'U': pygame.K_u,
            'V': pygame.K_v,
            'W': pygame.K_w,
            'X': pygame.K_x,
            'Y': pygame.K_y,
            'Z': pygame.K_z,
            'SPACE': pygame.K_SPACE,
            'CTRL': pygame.K_LCTRL,
            'LEFT': pygame.K_LEFT,
            'SHIFT_LEFT': pygame.K_LSHIFT
        }

        # Define Pygame key constants for controller
        self.pygame_key_mapping_controller = {
            'A': 0,
            'B': 1,
            'X': 2,
            'Y': 3,
            'LB': 4,
            'RB': 5,
            'SELECT': 6,
            'START': 7,
            'L3': 8,
            'R3': 9,
            'HOME': 10
        }

        # Read INI file
        self.config = configparser.ConfigParser()
        self.config.read(config_file_path)

        # Map INI values to Pygame key constants for keyboard
        self.key_dodge = self.get_pygame_key('keyboard', 'dodge')
        self.key_attack = self.get_pygame_key('keyboard', 'attack')
        self.key_sprint = self.get_pygame_key('keyboard', 'sprint')
        self.key_interact = self.get_pygame_key('keyboard', 'interact')
        self.key_move_up = self.get_pygame_key('keyboard', 'move_up')
        self.key_move_down = self.get_pygame_key('keyboard', 'move_down')
        self.key_move_left = self.get_pygame_key('keyboard', 'move_left')
        self.key_move_right = self.get_pygame_key('keyboard', 'move_right')
        self.key_movement = [self.key_move_up, self.key_move_down, self.key_move_left, self.key_move_right]

        self.btn_dodge = self.get_pygame_btn('controller', 'dodge')
        self.btn_sprint = self.get_pygame_btn('controller', 'sprint')
        self.btn_attack = self.get_pygame_btn('controller', 'attack')

    def check_user_input(self, keys, controller):
        ...

    def get_movement_vector(self, keys, controller) -> pygame.Vector2:
        """
        Returns the movement vector.
        :param keys: The pygame keyboard reading
        :param controller: The controller instance
        :return: The movement vector
        """

        mov_dir = pygame.Vector2(0, 0)

        if controller:
            if abs(controller.get_axis(0)) > self.CONTROLLER_DEAD_ZONE:
                mov_dir.x = controller.get_axis(0)
            if abs(controller.get_axis(1)) > self.CONTROLLER_DEAD_ZONE:
                mov_dir.y = controller.get_axis(1)

        if keys[self.key_move_up]:
            mov_dir.y = -1
        if keys[self.key_move_down]:
            mov_dir.y = 1
        if keys[self.key_move_left]:
            mov_dir.x = -1
        if keys[self.key_move_right]:
            mov_dir.x = 1

        return mov_dir

    def get_pygame_key(
            self,
            section: str,
            key: str
    ) -> int:
        """
        Returns the int value for action.
        :param section: The header for the ini subsection
        :param key: The key to use to extract the value
        :return: The key-bound statement
        """
        return self.pygame_key_mapping_keyboard.get(self.config[section].get(key, 'default_value'), pygame.K_UNKNOWN)

    def get_pygame_btn(
            self,
            section: str,
            key: str
    ) -> int:
        """
        Returns the int value for action.
        :param section: The header for the ini subsection
        :param key: The key to use to extract the value
        :return: The key-bound statement
        """
        return self.pygame_key_mapping_controller.get(self.config[section].get(key, 'default_value'), pygame.K_UNKNOWN)