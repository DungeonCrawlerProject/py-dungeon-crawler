from dataclasses import dataclass


@dataclass
class DoorWay:

    @dataclass
    class RoomSide:
        TOP: int
        RIGHT: int
        BOTTOM: int
        LEFT: int

    room_side = RoomSide
    is_able_to_generate = True
