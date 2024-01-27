"""
The HUD class which contains in game interfaces
By: Sean McClanahan
Last Modified: 12/31/23
"""

from Scripts.Player.player import Player
from Scripts.Engine.engine import GameEngine
from Scripts.UI.status_bar import StatusBar
from Scripts.UI.esc_menu import EscMenu
from Scripts.UI.settings_menu import SettingsMenu


class HUD:

    def __init__(
            self,
            player: Player,
            engine: GameEngine,
    ) -> None:
        """
        The HUD is a container for all GUI elements
        :param player: The player instance
        """
        self.player = player
        self.health_bar = StatusBar(50, 20, 200, 20, (255, 0, 0))
        self.stamina_bar = StatusBar(50, 50, 200, 20, (255, 255, 0))
        self.settings_menu = SettingsMenu(engine)
        self.esc_menu = EscMenu(engine, self.settings_menu)

    def update(self, esc_down, mouse_button_down, mouse_pos) -> None:
        """
        Updates the HUD using the attributes fed into the constructor
        """
        self.health_bar.update(100.0 * self.player.stats.current_health / self.player.stats.max_health)
        self.stamina_bar.update(100.0 * self.player.stats.current_stamina / self.player.stats.max_stamina)
        self.esc_menu.update(esc_down, mouse_button_down, mouse_pos)
        self.settings_menu.update(mouse_button_down, mouse_pos)

    def draw(self, screen) -> None:
        """
        Updates all graphics for the hud
        :param screen: The pygame screen
        """
        self.health_bar.draw(screen)
        self.stamina_bar.draw(screen)
        self.esc_menu.draw(screen)
        self.settings_menu.draw(screen)
