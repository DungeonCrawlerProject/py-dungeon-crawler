class MenuHandler:
    def __init__(self) -> None:
        pass

    def set_menus(self, esc_menu, setting_menu):
        self.esc_menu = esc_menu
        self.setting_menu = setting_menu
        self.current_menu = self.esc_menu

    def update_current(self, esc_down, mouse_button_down, mouse_pos):
        self.current_menu.update(esc_down, mouse_button_down, mouse_pos)

    def draw_current(self, screen):
        self.current_menu.draw(screen)

    def switch_menu(self, menu):
        self.current_menu = menu