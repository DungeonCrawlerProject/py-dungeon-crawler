"""
Player State Machine
By: Sean McClanahan
Last Modified: 01/27/2024
"""

from abc import (
    ABC,
    abstractmethod
)

from Scripts.Utility.game_controller import GameController


class IPlayerState(ABC):

    def __init__(self, player) -> None:
        """
        Handles the changing between player states
        :param player: The player instance
        """

        self.player = player

    @abstractmethod
    def update(self, game_controller: GameController) -> None:
        """
        Updates the players state, includes player movement and state switching
        :param game_controller: The Game Controller Instance
        """
        pass

    @abstractmethod
    def draw(self) -> None:
        """
        Changes the sprite for the character depending on the state
        """
        pass
