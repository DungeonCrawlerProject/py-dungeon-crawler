/*
Contains and updates the players stats
By: Nick Petruccelli
Last Modified: 08/19/2023
*/

using System;
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
    public List<string> equippedItems;
    public HealthBar healthBar;
    
    
    // Not going to lie some SerializeField went away this is what I think it is check it
    [SerializeField] private LayerMask layerMask;

    private void Start()
    {
        healthBar.SetHealth(curHealth);
    }

    public void TakeDamage(float damage)
    {
        curHealth -= damage;

        healthBar.SetHealth(curHealth/maxHealth);

        if (curHealth <= 0f)
        {
            Die();
        }
    }
    
    private void Die()
    {
        Instantiate(deathEffect, transform.position, Quaternion.identity);
        Destroy(gameObject);
    }
}
