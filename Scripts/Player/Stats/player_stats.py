"""
Contains and updates the players stats
By: Nick Petruccelli and Sean McClanahan
Last Modified: 12/26/2023
"""
from dataclasses import dataclass


@dataclass
class PlayerStats:

    # TODO make max_health and current health types a class where it is floored and ceiling to the maxes/mins
    max_health: float = 10.0
    current_health: float = 10.0

    max_stamina: float = 100.0
    current_stamina: float = 100.0

    sprint_factor: float = 1.5
    speed: float = 7.5

    dodge_distance: float = 125.0
    dodge_cooldown: float = 2.0
