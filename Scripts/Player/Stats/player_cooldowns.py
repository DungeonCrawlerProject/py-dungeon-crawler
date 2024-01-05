"""
Contains and updates the player's active cooldown timers
By: Sean McClanahan
Last Modified: 12/31/2023
"""
from dataclasses import dataclass


@dataclass
class PlayerCoolDownTimer:
    dodge_cooldown_timer: float = 0.0
