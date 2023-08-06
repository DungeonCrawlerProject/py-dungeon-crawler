/*
Contains and updates the players stats
By: Nick Petruccelli
Last Modified: 08/06/2023
*/

using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerStats : MonoBehaviour
{
    public float plyrMaxHealth = 10f;
    public float plyrCurHealth = 10f;
    public float plyrDamageMult = 1f;

    public float getDamageMult()
    {
        return plyrDamageMult;
    }
}
