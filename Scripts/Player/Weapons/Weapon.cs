/*
Generic weapon class that stores basic wepon info
By: Nick Petruccelli
Last Modified: 08/10/2023
*/

using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Weapon : MonoBehaviour
{
    public string wepName;
    public float damage;
    public float critChance;
    public float critMultiplier;
    public GameObject groundItem;
    public float pickUpOffSet;

}
