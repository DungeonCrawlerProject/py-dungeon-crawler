using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class DungeonGeneration : MonoBehaviour
{
    public GameObject spawnRoom;
    public Vector3 spawnRoomLocation;
    public List<GameObject> largeRooms;
    public List<GameObject> smallRooms;
    public List<GameObject> hallWays;
    public LayerMask roomMask;
    public int mapWidth = 50;
    public int mapHight = 50;
    public int largeRoomTarget = 1;
    public int smallRoomTarget = 1;
    public int loopMax = 100;
    public List<GameObject> placedRooms;
    public List<GameObject> availableRooms;

    private Vector2 roomPosition = Vector2.zero;
    private Vector2 roomOffSet = Vector2.zero;
    private Vector2 roomExtents = Vector2.zero;
    private GameObject room;
    private GameObject newDoorWay;
    private int roomSize;
    private Collider2D detectedRoom = null;
    private List<GameObject> roomTypeToGen;
    private Room existingRoomScript;
    private GameObject doorWay;
    private int doorWayDir;

    void Awake()
    {
        Generate();
    }

    void Generate()
    {
        // Place Spawn Room
        GameObject _spawnRoom = Instantiate(spawnRoom, spawnRoomLocation, Quaternion.identity);
        placedRooms.Add(_spawnRoom);

        // create loop that generates rooms off of preexisting doorways
        while (loopMax > 0)
        {
            // randomly select a doorway and check if it can generate a room
            bool goodDoor = false;
            while (goodDoor == false)
            {
                existingRoomScript = placedRooms[Random.Range(0, placedRooms.Count)].GetComponent<Room>();
                doorWay = existingRoomScript.doorWays[Random.Range(0, existingRoomScript.doorWays.Count)];
                doorWayDir = (int)doorWay.GetComponent<DoorWay>().roomSide;

                if (doorWay.GetComponent<DoorWay>().isAbleToGenerate)
                {
                    goodDoor = true;
                }
            }            

            // Determine what type of rooms can be placed and randomly chose a room among available room types
            int roomType = (int)existingRoomScript.roomType;
            
            if (roomType != 3)
            {
                int doorWayDirNeeded = (doorWayDir + 2) % 4;
                foreach (GameObject _room in hallWays)
                {
                    foreach (GameObject _doorWay in _room.GetComponent<Room>().doorWays)
                    {
                        if ((int)_doorWay.GetComponent<DoorWay>().roomSide == doorWayDirNeeded)
                        {
                            availableRooms.Add(_room);
                        }
                    }
                }

                // Pick random room from available rooms
                room = availableRooms[Random.Range(0, availableRooms.Count)];

                // refind corect doorway and set roomOffSet
                foreach (GameObject _doorWay in room.GetComponent<Room>().doorWays)
                {
                    if ((int)_doorWay.GetComponent<DoorWay>().roomSide == doorWayDirNeeded)
                    {

                        roomOffSet.x = -(_doorWay.transform.position.x);
                        roomOffSet.y = -(_doorWay.transform.position.y);
                    }
                }

                // Get size of room and check if it has space to be placed
                roomExtents = room.GetComponent<BoxCollider2D>().size;

                roomPosition.x = doorWay.transform.position.x + roomOffSet.x;
                roomPosition.y = doorWay.transform.position.y + roomOffSet.y;

                detectedRoom = Physics2D.OverlapBox(point: roomPosition, size: roomExtents - new Vector2(.25f, .25f), angle: 0f, layerMask: roomMask);                    

                // Place room if not collisions detected and add to placed rooms list
                if (detectedRoom == null)
                {
                    GameObject placedRoom = Instantiate(room, roomPosition, Quaternion.identity);
                    placedRooms.Add(placedRoom);

                    // keep used doorways from spawing any mor rooms
                    doorWay.GetComponent<DoorWay>().isAbleToGenerate = false;
                    foreach (GameObject _doorWay in placedRoom.GetComponent<Room>().doorWays)
                    {
                        if ((int)_doorWay.GetComponent<DoorWay>().roomSide == doorWayDirNeeded)
                        {
                            _doorWay.GetComponent<DoorWay>().isAbleToGenerate = false;
                        }
                        else
                        {
                            _doorWay.GetComponent<DoorWay>().isAbleToGenerate = true;
                        }
                    }
                }
            }
            else
            {
                int doorWayDirNeeded = (doorWayDir + 2) % 4;

                // Select room Type
                if (Random.Range(0f, 1f) <= .80f)
                {
                    if (Random.Range(0f, 1f) <= .50f)
                    {
                        if (largeRoomTarget > 0)
                        {
                            roomTypeToGen = largeRooms;
                        }
                        else
                        {
                            roomTypeToGen = smallRooms;
                        }
                    }
                    else
                    {
                        if (smallRoomTarget > 0)
                        {
                            roomTypeToGen = smallRooms;
                        }
                        else
                        {
                            roomTypeToGen = largeRooms;
                        }
                    }
                }
                else
                {
                    roomTypeToGen = hallWays;
                }
                

                // Create list of available rooms to place
                foreach (GameObject _room in roomTypeToGen)
                {
                    foreach (GameObject _doorWay in _room.GetComponent<Room>().doorWays)
                    {
                        if ((int)_doorWay.GetComponent<DoorWay>().roomSide == doorWayDirNeeded)
                        {
                            availableRooms.Add(_room);
                        }
                    }
                }

                // Pick random room from available rooms
                room = availableRooms[Random.Range(0, availableRooms.Count)];

                // refind corect doorway and set roomOffSet
                foreach (GameObject _doorWay in room.GetComponent<Room>().doorWays)
                {
                    if ((int)_doorWay.GetComponent<DoorWay>().roomSide == doorWayDirNeeded)
                    {

                        roomOffSet.x = -(_doorWay.transform.position.x);
                        roomOffSet.y = -(_doorWay.transform.position.y);
                        newDoorWay = _doorWay;
                    }
                }

                // Get size of room and check if it has space to be placed
                roomExtents = room.GetComponent<BoxCollider2D>().size;

                roomPosition.x = doorWay.transform.position.x + roomOffSet.x;
                roomPosition.y = doorWay.transform.position.y + roomOffSet.y;

                detectedRoom = Physics2D.OverlapBox(point: roomPosition, size: roomExtents - new Vector2(.25f, .25f), angle: 0f, layerMask: roomMask);

                if (detectedRoom == null)
                {
                    GameObject placedRoom = Instantiate(room, roomPosition, Quaternion.identity);
                    placedRooms.Add(placedRoom);

                    // keep used doorways from spawing any mor rooms
                    doorWay.GetComponent<DoorWay>().isAbleToGenerate = false;
                    foreach (GameObject _doorWay in placedRoom.GetComponent<Room>().doorWays)
                    {
                        if ((int)_doorWay.GetComponent<DoorWay>().roomSide == doorWayDirNeeded)
                        {
                            _doorWay.GetComponent<DoorWay>().isAbleToGenerate = false;
                        }
                        else
                        {
                            _doorWay.GetComponent<DoorWay>().isAbleToGenerate = true;
                        }
                    }

                    // Adust target room counter
                    if (placedRoom.GetComponent<Room>().roomSize == 0 && (int)placedRoom.GetComponent<Room>().roomType != 3)
                    {
                        smallRoomTarget -= 1;
                    }
                    else if((int)placedRoom.GetComponent<Room>().roomSize == 2 && (int)placedRoom.GetComponent<Room>().roomType != 3)
                    {
                        largeRoomTarget -= 1;
                    }

                }
            }
            detectedRoom = null;
            availableRooms.Clear();
            roomOffSet = Vector2.zero;
            loopMax -= 1;

            // check if target room count has been reached
            if (largeRoomTarget <= 0 && smallRoomTarget <= 0)
            {
                break;
            } 
        }

    }   
}
