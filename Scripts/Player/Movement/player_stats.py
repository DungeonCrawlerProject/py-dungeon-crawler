"""
Contains and updates the players stats
By: Nick Petruccelli and Sean McClanahan
Last Modified: 12/26/2023
"""


class PlayerStats:

    max_health: float = 10.0
    current_health: float = 10.0
    damage_mult: float = 1.0
    crit_chance: float = 0.0
    crit_multiplier: float = 1.0
    sprint_factor: float = 1.5
    speed: float = 7.5

    def __init__(self):
        # Once healthbar is implemented, set healthbar health
        # healthBar.SetHealth(curHealth);
        ...


