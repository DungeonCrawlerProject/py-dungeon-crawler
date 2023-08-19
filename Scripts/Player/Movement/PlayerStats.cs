/*
Contains and updates the players stats
By: Nick Petruccelli
Last Modified: 08/19/2023
*/

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
    
    // Not going to lie some SerializeField went away this is what I think it is check it
    [SerializeField] private LayerMask layerMask;
    
    public void TakeDamage(float damage)
    {
        curHealth -= damage;

        if (true)
        {
            UseFakeHealthBar();
        }

        if (curHealth <= 0f)
        {
            Die();
        }
    }
    
    private void UseFakeHealthBar()
    {
        // For Variables that don't change throw in a const prefix
        const string filled = "X";
        const string empty = "-";
		
        string healthBar = "";
		
        int percentage = (int)Mathf.Round(curHealth/maxHealth*100);
		
        for (int i=0; i<=percentage; i++) {
            healthBar += filled;
        }
        for (int j=0; j<=(100-percentage); j++) {
            healthBar += empty;
        }
		
        Debug.Log(healthBar);
    }
    
    private void Die()
    {
        Instantiate(deathEffect, transform.position, Quaternion.identity);
        Destroy(gameObject);
    }
}
