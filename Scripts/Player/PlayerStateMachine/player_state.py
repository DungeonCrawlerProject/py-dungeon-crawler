"""
Player State Machine
By: Sean McClanahan
Last Modified: 01/04/2024
"""

from abc import (
    ABC,
    abstractmethod
)


class IPlayerState(ABC):

    def __init__(self, player) -> None:
        """
        Handles the changing between player states
        :param player: The player instance
        """

        self.player = player

    @abstractmethod
    def update(self, keys, controller) -> None:
        """
        Updates the players state, includes player movement and state switching
        :param keys: The pygame input keys
        :param controller: The controller instance
        """
        pass

    @abstractmethod
    def draw(self) -> None:
        """
        Changes the sprite for the character depending on the state
        """
        pass
