using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class DungeonGeneration : MonoBehaviour
{
    public GameObject spawnRoom;
    public Vector3 spawnRoomLocation;
    public List<GameObject> largeRooms;
    public List<GameObject> smallRooms;
    public LayerMask roomMask;
    public int mapWidth = 50;
    public int mapHight = 50;
    public int largeRoomTarget = 1;
    public int smallRoomTarget = 1;
    public int loopMax = 100;

    private Vector2 roomPosition = Vector2.zero;
    private Vector2 roomHalfExtents = Vector2.zero;
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
}
