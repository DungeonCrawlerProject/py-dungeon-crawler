"""
Contains and updates the player's active cooldown timers
By: Sean McClanahan
Last Modified: 12/31/2023
"""
from dataclasses import dataclass

from Scripts.Utility.cronos_clock import CronosClock


@dataclass
class PlayerCoolDownTimer:
    dodge = CronosClock()
