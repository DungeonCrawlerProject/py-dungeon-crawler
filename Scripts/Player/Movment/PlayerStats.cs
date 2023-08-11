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
    public float maxHealth = 10f;
    public float curHealth = 10f;
    public float damageMult = 1f;
    public float critChance = 0;
    public float critMultiplier = 1;
    public ParticleSystem deathEffect;
    public List<string> equipedItems;

    public void takeDamage(float damage)
    {
        curHealth -= damage;

        if (curHealth <= 0f)
        {
            Die();
        }
    }

    void Die()
    {
        Instantiate(deathEffect, transform.position, Quaternion.identity);
        Destroy(gameObject);
    }
}
