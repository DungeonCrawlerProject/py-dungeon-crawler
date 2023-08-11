/*
Generic ranged weapon class that stores basic weapon info and sooting function
By: Nick Petruccelli
Last Modified: 08/10/2023
*/

using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class RangedWeapon : Weapon
{
    public Transform firePoint;
    public GameObject bulletPreFab;
    public float bulletForce = 25f;
    public float fireDelay = .25f;
    
    private float lastFireTime;
    private float damageFinal;
    private float critChanceFinal;
    

    // Start is called before the first frame update
    void Start()
    {
        lastFireTime = -fireDelay;
        PlayerStats playerStats = transform.parent.GetComponent<PlayerStats>();
        damageFinal = damage * playerStats.damageMult;
        critChanceFinal = critChance + playerStats.critChance;
    }

    // Update is called once per frame
    void Update()
    {
        if (Input.GetButton("Fire1") && (lastFireTime + fireDelay < Time.time))
        {
            Shoot();
            lastFireTime = Time.time;
        }
    }

    void Shoot()
    {
        // Instantiate bullet and access its rigid body
        GameObject bullet = Instantiate(bulletPreFab, firePoint.position, firePoint.rotation);
        Rigidbody2D rb = bullet.GetComponent<Rigidbody2D>();
        Bullet bulletScript = bullet.GetComponent<Bullet>();

        // Determine if bullet is going to crit and adjust damage if it does
        float random = Random.Range(0,1);
        float damageTemp = damageFinal;
        if (critChance >= random)
        {
            damageFinal = damageFinal * critMultiplier;
        }

        // Apply damage to bullet and move it foward
        bulletScript.SetDamage(damageFinal);
        rb.AddForce(firePoint.up * bulletForce, ForceMode2D.Impulse);

        // Reset damage back to non crit damage
        damageFinal = damageTemp;

    }
}
