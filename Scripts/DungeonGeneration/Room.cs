using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Room : MonoBehaviour
{
    public enum RoomSize
    {
        small,
        medium,
        large
    }
    public enum RoomType
    {
        spawn,
        room,
        boss,
        hall
    }
    public RoomSize roomSize;
    public RoomType roomType;
    public List<GameObject> doorWays;
}
