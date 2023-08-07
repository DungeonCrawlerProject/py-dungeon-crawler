/*
Controls the enemy movment and shooting ai
By: Nick Petruccelli
Last Modified: 08/06/2023
*/

using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Pathfinding;

public class Enemy : MonoBehaviour
{

    public float hP = 20f;
    public float agroRange = 20f;
    public float fireRange= 15f;
    public ParticleSystem deathEffect;
    public float fireRate;
    public float enemyDamage;
    public GameObject bulletPreFab;
    public Transform firePoint;
    public float bulletForce = 15f;
    public float rotationSpeed = 20;
    public float rotationOffSet = 0;

    private float damage;
    private Transform player;
    private float lastFireTime;
    private AIPath path;
    [SerializeField] private LayerMask layerMask;

    void Start()
    {
        // Locate the player gameObject
        player = GameObject.FindGameObjectWithTag("Player").transform;

        // Initilizes shot reset timer
        lastFireTime = -fireRate;

        // Get A* Script
        path = gameObject.GetComponent<AIPath>();
    }

    void Update()
    {
        // Cast ray from enemy to player to see if wall is in between player and enemy
        RaycastHit2D ray = Physics2D.Raycast(transform.position, player.transform.position - transform.position, fireRange, layerMask);
        Debug.DrawRay(transform.position, player.transform.position - transform.position, Color.red);
        
        // If ray does not hit enviorment look at player and shoot.
        if (ray.collider.tag == "Player")
        {
            LookAtPlayer();
            if (lastFireTime + fireRate < Time.time)
            {
                Shoot();
                lastFireTime = Time.time;
            }
           
        }      

    }

    public void takeDamage(float damage)
    {
        hP = hP - damage;

        if(hP <= 0f)
        {
            Die();
        }
    }

    void Die()
    {
        Instantiate(deathEffect, transform.position, Quaternion.identity);
        Destroy(gameObject);
    }

    void Shoot()
    {
        GameObject bullet = Instantiate(bulletPreFab, firePoint.position, firePoint.rotation);
        Rigidbody2D rb = bullet.GetComponent<Rigidbody2D>();
        EnemyBullet bulletScript = bullet.GetComponent<EnemyBullet>();
        bulletScript.SetDamage(enemyDamage);
        rb.AddForce(firePoint.up * bulletForce, ForceMode2D.Impulse);
    }

    void LookAtPlayer()
    {
        Vector2 lookDir = player.transform.position - transform.position;
        float angle = (Mathf.Atan2(lookDir.y, lookDir.x) * Mathf.Rad2Deg) - rotationOffSet;
        Quaternion q = Quaternion.AngleAxis(angle, Vector3.forward);
        transform.rotation = Quaternion.Slerp(transform.rotation, q, Time.deltaTime * rotationSpeed);
    }
}
