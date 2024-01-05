import pygame

from Scripts.Player.PlayerStateMachine.player_state import IPlayerState


class IdleState(IPlayerState):
    def update(self, keys):
        if keys[pygame.K_w] or keys[pygame.K_a] or keys[pygame.K_s] or keys[pygame.K_d]:
            self.player.state = self.player.moving_state_inst
        elif keys[pygame.K_SPACE]:
            self.player.state = self.player.dodge_state_inst
        elif keys[pygame.K_LSHIFT]:
            self.player.state = self.player.sprinting_state_inst
        else:
            self.player.stats.current_stamina += 2.0
            self.player.stats.current_stamina = min(self.player.stats.current_stamina, self.player.stats.max_stamina)

    def draw(self):
        self.player.sprite.image = self.player.sprite.frames[0]
