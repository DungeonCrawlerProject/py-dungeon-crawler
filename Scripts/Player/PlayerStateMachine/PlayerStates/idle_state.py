"""
Idle State
By: Sean McClanahan
Last Modified: 02/03/2024
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
            self.player.moving_state_inst.momentum_timer.restart_time()

            # Start both animations for them to be in sync
            self.player.animations["walk"].start_animation()
            self.player.animations["walk_side"].start_animation()
        else:
            self.idle()

    def idle(self):
        pass

    def draw(self) -> None:
        """
        Changes the sprite for the character depending on the state
        """
        self.player.game_obj["player"].sprite.change_frame(0)
        self.player.game_obj["player"].sprite.visible = True
