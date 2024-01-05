"""
The HUD class which contains in game interfaces
By: Sean McClanahan
Last Modified: 12/31/23
"""

from Scripts.Player.player import Player
from Scripts.UI.status_bar import StatusBar


class HUD:

    def __init__(
            self,
            player: Player
    ) -> None:
        """
        The HUD is a container for all GUI elements
        :param player: The player instance
        """
        self.player = player
        self.health_bar = StatusBar(50, 20, 200, 20, (255, 0, 0))
        self.stamina_bar = StatusBar(50, 50, 200, 20, (255, 255, 0))

    def update(self) -> None:
        """
        Updates the HUD using the attributes fed into the constructor
        """
        self.health_bar.update(100.0 * self.player.stats.current_health / self.player.stats.max_health)
        self.stamina_bar.update(100.0 * self.player.stats.current_stamina / self.player.stats.max_stamina)

    def draw(self, screen) -> None:
        """
        Updates all graphics for the hud
        :param screen: The pymunk screen
        """

        self.health_bar.draw(screen)
        self.stamina_bar.draw(screen)
