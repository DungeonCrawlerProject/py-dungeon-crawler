"""
Contains and updates the players stats
By: Nick Petruccelli
Last Modified: 08/19/2023
"""


class PlayerStats:

    maxHealth: float = 10.0
    curHealth: float = 10.0
    damageMult: float = 1.0
    critChance: float = 0.0
    critMultiplier: float = 1.0

    def __init__(self):
        # Once healthbar is implemented, set healthbar health
        # healthBar.SetHealth(curHealth);
        ...

    # TODO take damage should be a player based item that inflicts it player stat dataclass
    def take_damage(self, damage: float):
        self.curHealth -= damage

        # healthBar.SetHealth(curHealth / maxHealth);

        if self.curHealth < 0:
            self.kill_player()

    # TODO same is for the kill player command
    def kill_player(self):
        ...
