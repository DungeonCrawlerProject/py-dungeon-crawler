/*
Controls players shooting
By: Nick Petruccelli
Last Modified: 08/06/2023
*/

using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Shooting : MonoBehaviour
{

    public Transform firePoint;
    public GameObject bulletPreFab;
    public float bulletForce = 25f;
    public float fireDelay = .25f;
    public float wepDamage = 10f;

    private float lastFireTime;
    private float damage;

    void Start()
    {
        lastFireTime = -fireDelay;
        PlayerStats playerStats = gameObject.GetComponent<PlayerStats>();
        damage = wepDamage * playerStats.getDamageMult();
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
        GameObject bullet = Instantiate(bulletPreFab, firePoint.position, firePoint.rotation);
        Rigidbody2D rb = bullet.GetComponent<Rigidbody2D>();
        Bullet bulletScript = bullet.GetComponent<Bullet>();
        bulletScript.SetDamage(damage);
        rb.AddForce(firePoint.up * bulletForce, ForceMode2D.Impulse);

    }
}
