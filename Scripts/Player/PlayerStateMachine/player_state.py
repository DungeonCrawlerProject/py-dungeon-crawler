"""
Player State Machine
By: Sean McClanahan
Last Modified: 12/31/2023
"""

from abc import ABC, abstractmethod


class IPlayerState(ABC):

    def __init__(self, player) -> None:
        self.player = player

    @abstractmethod
    def update(self, keys):
        pass

    @abstractmethod
    def draw(self):
        pass
