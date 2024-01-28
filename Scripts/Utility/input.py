from dataclasses import dataclass


@dataclass
class Input:
    DODGE: str = 'dodge'
    SPRINT: str = 'sprint'
    BLOCK: str = 'block'
    ATTACK: str = 'attack'
    INTERACT: str = 'interact'
    MOVE_UP: str = 'move_up'
    MOVE_DOWN: str = 'move_down'
    MOVE_LEFT: str = 'move_left'
    MOVE_RIGHT: str = 'move_right'
    OMIT: str = 'OMIT'
