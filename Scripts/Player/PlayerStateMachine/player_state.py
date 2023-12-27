from abc import ABC, abstractmethod


class IPlayerState(ABC):
    @abstractmethod
    def do_state(self, player):
        pass
