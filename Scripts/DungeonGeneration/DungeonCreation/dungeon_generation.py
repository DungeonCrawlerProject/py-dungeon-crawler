from typing import Tuple, List

from Scripts.DungeonGeneration.DungeonCreation.room import Room


class DungeonGeneration:

    def __init__(self):
        self.spawnRoom = None
        self.spawn_room_location: Tuple[float, float]

        self.large_rooms = List[Room]
        self.small_rooms = List[Room]
        self.hall_ways = List[Room]

        self.door_fill = None
        self.room_mask = None
        self.map_width: int = 50
        self.map_height: int = 50
        self.large_room_target: int = 1
        self.small_room_target: int = 1
        self.loop_max: int = 100

        self.placed_rooms = List[Room]
        self.available_rooms = List[Room]

        # Privates
        self._roomPosition = (0, 0)
        self._roomOffSet = (0, 0)
        self._roomExtents = (0, 0)
        self._room = None
        self._new_door_way = None
        self._room_size: int = None
        self._detected_room = None
        self._room_type_to_gen: List[Room] = None
        self._existingRoomScript: Room = None
        self._doorWay = None
        self._doorWayDir: int

        # Generate The Dungeon
        self.generate()


    def generate(self):

        raise NotImplementedError

        # // Place Spawn Room
        # GameObject _spawnRoom = Instantiate(spawnRoom, spawnRoomLocation, Quaternion.identity);
        # placedRooms.Add(_spawnRoom);
        #
        # // create loop that generates rooms off of preexisting doorways
        # while (loopMax > 0) {
        #     // randomly select a doorway and check if it can generate a room
        #     bool goodDoor = false;
        #     while (goodDoor == false) {
        #         existingRoomScript = placedRooms[Random.Range(0, placedRooms.Count)].GetComponent<Room>();
        #         doorWay = existingRoomScript.doorWays[Random.Range(0, existingRoomScript.doorWays.Count)];
        #         doorWayDir = (int)doorWay.GetComponent<DoorWay>().roomSide;
        #
        #         if (doorWay.GetComponent<DoorWay>().isAbleToGenerate) {
        #             goodDoor = true;
        #         }
        #     }
        #
        #     // Determine what type of rooms can be placed and randomly chose a room among available room types
        #     int roomType = (int)existingRoomScript.roomType;
        #
        #     if (roomType != 3) {
        #         int doorWayDirNeeded = (doorWayDir + 2) % 4;
        #         foreach (GameObject _room in hallWays) {
        #             foreach (GameObject _doorWay in _room.GetComponent<Room>().doorWays) {
        #                 if ((int)_doorWay.GetComponent<DoorWay>().roomSide == doorWayDirNeeded) {
        #                     availableRooms.Add(_room);
        #                 }
        #             }
        #         }
        #
        #         // Pick random room from available rooms
        #         room = availableRooms[Random.Range(0, availableRooms.Count)];
        #
        #         // refind corect doorway and set roomOffSet
        #         foreach (GameObject _doorWay in room.GetComponent<Room>().doorWays) {
        #             if ((int)_doorWay.GetComponent<DoorWay>().roomSide == doorWayDirNeeded) {
        #                 roomOffSet.x = -(_doorWay.transform.position.x);
        #                 roomOffSet.y = -(_doorWay.transform.position.y);
        #             }
        #         }
        #
        #         // Get size of room and check if it has space to be placed
        #         roomExtents = room.GetComponent<BoxCollider2D>().size;
        #
        #         roomPosition.x = doorWay.transform.position.x + roomOffSet.x;
        #         roomPosition.y = doorWay.transform.position.y + roomOffSet.y;
        #
        #         detectedRoom = Physics2D.OverlapBox(point: roomPosition, size: roomExtents - new Vector2(.25f, .25f), angle: 0f, layerMask: roomMask);
        #
        #         // Place room if not collisions detected and add to placed rooms list
        #         if (detectedRoom == null) {
        #             GameObject placedRoom = Instantiate(room, roomPosition, Quaternion.identity);
        #             placedRooms.Add(placedRoom);
        #
        #             // keep used doorways from spawing any mor rooms
        #             doorWay.GetComponent<DoorWay>().isAbleToGenerate = false;
        #             foreach (GameObject _doorWay in placedRoom.GetComponent<Room>().doorWays) {
        #                 if ((int)_doorWay.GetComponent<DoorWay>().roomSide == doorWayDirNeeded) {
        #                     _doorWay.GetComponent<DoorWay>().isAbleToGenerate = false;
        #                 } else {
        #                     _doorWay.GetComponent<DoorWay>().isAbleToGenerate = true;
        #                 }
        #             }
        #         }
        #     } else {
        #         int doorWayDirNeeded = (doorWayDir + 2) % 4;
        #
        #         // Select room Type
        #         if (Random.Range(0f, 1f) <= .80f) {
        #             if (Random.Range(0f, 1f) <= .50f) {
        #                 if (largeRoomTarget > 0) {
        #                     roomTypeToGen = largeRooms;
        #                 } else {
        #                     roomTypeToGen = smallRooms;
        #                 }
        #             } else {
        #                 if (smallRoomTarget > 0) {
        #                     roomTypeToGen = smallRooms;
        #                 } else {
        #                     roomTypeToGen = largeRooms;
        #                 }
        #             }
        #         } else {
        #             roomTypeToGen = hallWays;
        #         }
        #
        #         // Create list of available rooms to place
        #         foreach (GameObject _room in roomTypeToGen) {
        #             foreach (GameObject _doorWay in _room.GetComponent<Room>().doorWays) {
        #                 if ((int)_doorWay.GetComponent<DoorWay>().roomSide == doorWayDirNeeded) {
        #                     availableRooms.Add(_room);
        #                 }
        #             }
        #         }
        #
        #         // Pick random room from available rooms
        #         room = availableRooms[Random.Range(0, availableRooms.Count)];
        #
        #         // refind corect doorway and set roomOffSet
        #         foreach (GameObject _doorWay in room.GetComponent<Room>().doorWays) {
        #             if ((int)_doorWay.GetComponent<DoorWay>().roomSide == doorWayDirNeeded) {
        #
        #                 roomOffSet.x = -(_doorWay.transform.position.x);
        #                 roomOffSet.y = -(_doorWay.transform.position.y);
        #                 newDoorWay = _doorWay;
        #             }
        #         }
        #
        #         // Get size of room and check if it has space to be placed
        #         roomExtents = room.GetComponent<BoxCollider2D>().size;
        #
        #         roomPosition.x = doorWay.transform.position.x + roomOffSet.x;
        #         roomPosition.y = doorWay.transform.position.y + roomOffSet.y;
        #
        #         detectedRoom = Physics2D.OverlapBox(point: roomPosition, size: roomExtents - new Vector2(.25f, .25f), angle: 0f, layerMask: roomMask);
        #
        #         if (detectedRoom == null)  {
        #             GameObject placedRoom = Instantiate(room, roomPosition, Quaternion.identity);
        #             placedRooms.Add(placedRoom);
        #
        #             // keep used doorways from spawing any mor rooms
        #             doorWay.GetComponent<DoorWay>().isAbleToGenerate = false;
        #             foreach (GameObject _doorWay in placedRoom.GetComponent<Room>().doorWays) {
        #                 if ((int)_doorWay.GetComponent<DoorWay>().roomSide == doorWayDirNeeded) {
        #                     _doorWay.GetComponent<DoorWay>().isAbleToGenerate = false;
        #                 } else {
        #                     _doorWay.GetComponent<DoorWay>().isAbleToGenerate = true;
        #                 }
        #             }
        #
        #             // Adust target room counter
        #             if (placedRoom.GetComponent<Room>().roomSize == 0 && (int)placedRoom.GetComponent<Room>().roomType != 3) {
        #                 smallRoomTarget -= 1;
        #             } else if((int)placedRoom.GetComponent<Room>().roomSize == 2 && (int)placedRoom.GetComponent<Room>().roomType != 3) {
        #                 largeRoomTarget -= 1;
        #             }
        #
        #         }
        #     }
        #     detectedRoom = null;
        #     availableRooms.Clear();
        #     roomOffSet = Vector2.zero;
        #     loopMax -= 1;
        #
        #     // check if target room count has been reached
        #     if (largeRoomTarget <= 0 && smallRoomTarget <= 0) {
        #         break;
        #     }
        # }
        #
        # // Fill in unused doorways
        # foreach (GameObject _room in placedRooms) {
        #     foreach (GameObject _doorWay in _room.GetComponent<Room>().doorWays) {
        #         DoorWay _doorWayScript = _doorWay.GetComponent<DoorWay>();
        #         if (_doorWayScript.isAbleToGenerate == true) {
        #             switch ((int)_doorWayScript.roomSide) {
        #                 case 0:
        #                     Instantiate(doorFill, _doorWay.transform.position + new Vector3(0f,-.5f,0f), Quaternion.Euler(0f,0f,0f));
        #                     break;
        #                 case 1:
        #                     Instantiate(doorFill, _doorWay.transform.position + new Vector3(-.5f, 0f, 0f), Quaternion.Euler(0f, 0f, 90f));
        #                     break;
        #                 case 2:
        #                     Instantiate(doorFill, _doorWay.transform.position + new Vector3(0f, .5f, 0f), Quaternion.Euler(0f, 0f, 0f));
        #                     break;
        #                 case 3:
        #                     Instantiate(doorFill, _doorWay.transform.position + new Vector3(.5f, 0f, 0f), Quaternion.Euler(0f, 0f, 90f));
        #                     break;
        #             }
        #         }
        #     }
        # }
        #
        # // Recalculate Ai pathfinding
        # AstarPath.active.Scan();
