from dataclasses import dataclass
from enum import Enum
from typing import List

from Scripts.DungeonGeneration.DungeonCreation.door_way import DoorWay


@dataclass
class Room:

    class RoomSize(Enum):
        SMALL = 1
        MEDIUM = 2
        LARGE = 3

    class RoomType(Enum):
        SPAWN = 1
        ROOM = 2
        BOSS = 3
        HALL = 4

    room_size: RoomSize
    room_type: RoomType
    door_ways: List[DoorWay]
