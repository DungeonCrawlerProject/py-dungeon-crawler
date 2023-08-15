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
    private int roomSize;
    private Collider2D detectedRoom = null;
    
    void Awake()
    {
        Generate();
    }

    void Generate()
    {
        // Place Spawn Room
        GameObject _spawnRoom = (GameObject)Instantiate(spawnRoom, spawnRoomLocation, Quaternion.identity);
        placedRooms.Add(_spawnRoom);

        // create loop that generates rooms off of preexisting doorways
        while ((largeRoomTarget > 0 || smallRoomTarget > 0) && loopMax > 0)
        {
            // randomly select a doorway
            Room existingRoomScript = placedRooms[Random.Range(0, placedRooms.Count)].GetComponent<Room>();
            GameObject doorWay = existingRoomScript.doorWays[Random.Range(0, existingRoomScript.doorWays.Count)];
            int doorWayDir = (int)doorWay.GetComponent<DoorWay>().roomSide;

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

                detectedRoom = Physics2D.OverlapBox(point: roomPosition, size: roomExtents - new Vector2(.25f,.25f), angle: 0f, layerMask: roomMask);
;

                if (detectedRoom == null)
                {
                    Instantiate(room, roomPosition, Quaternion.identity);

                    if (roomSize == 1)
                    {
                        smallRoomTarget -= 1;
                    }
                    else
                    {
                        largeRoomTarget -= 1;
                    }
                }

                detectedRoom = null;
                roomOffSet = Vector2.zero;
                loopMax -= 1;
            }
            break;
        }

    }

    /*
    void Generate()
    {
        // Place Spawn Room
        Instantiate(spawnRoom, spawnRoomLocation, Quaternion.identity);

        // Generate Random x and y cords for next room to be generated
        while ((largeRoomTarget > 0 || smallRoomTarget > 0) && loopMax > 0)
        {
            roomPosition.x = Mathf.Round(Random.Range(-mapWidth, mapWidth));
            roomPosition.y = Mathf.Round(Random.Range(-mapHight, mapHight));

            // randomly select if room will be large or small
            if (Random.Range(0f,1f) < .5 && smallRoomTarget > 0)
            {
                roomSize = 1;
                room = smallRooms[Random.Range(0, smallRooms.Count - 1)];
            }
            else if (largeRoomTarget > 0)
            {
                roomSize = 2;
                room = largeRooms[Random.Range(0, largeRooms.Count - 1)];
            }
            else
            {
                roomSize = 1;
                room = smallRooms[Random.Range(0, smallRooms.Count - 1)];
            }
 
            // Get size of rooms box collider
            roomHalfExtents.x = room.GetComponent<BoxCollider2D>().size.x;
            roomHalfExtents.y = room.GetComponent<BoxCollider2D>().size.y;
            
            // check if room to be placed's collider is intersecting with another pre-existing room
            detectedRoom = Physics2D.OverlapBox(point: roomPosition,size: roomHalfExtents,angle: 0f,layerMask: roomMask);
            
            if (detectedRoom == null)
            {
                Instantiate(room, roomPosition, Quaternion.identity);

                if(roomSize == 1)
                {
                    smallRoomTarget -= 1;
                }
                else
                {
                    largeRoomTarget -= 1;
                }
            }

            detectedRoom = null;
            loopMax -= 1;
        }
    }
    */
}
