"""
Generic weapon class that stores basic weapon info
By: Nick Petruccelli
Last Modified: 12/26/2023
"""
from dataclasses import dataclass


@dataclass
class Weapon:
    weapon_name: str
    base_damage: float
    crit_chance: float
    crit_mult: float
