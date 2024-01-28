"""
Idle State
By: Sean McClanahan
Last Modified: 01/27/2024
"""

from Scripts.Utility.game_controller import GameController
from Scripts.Player.PlayerStateMachine.player_state import IPlayerState


class IdleState(IPlayerState):

    def update(self, game_controller: GameController) -> None:
        """
        Updates the players state, includes player movement and state switching
        :param game_controller: The Game Controller Instance
        """

        if game_controller.is_moving():
            self.player.state = self.player.moving_state_inst
        else:
            self.player.stats.current_stamina += 2.0
            self.player.stats.current_stamina = min(self.player.stats.current_stamina, self.player.stats.max_stamina)

    def draw(self) -> None:
        """
        Changes the sprite for the character depending on the state
        """
        self.player.sprite.image = self.player.sprite.frames[0]
