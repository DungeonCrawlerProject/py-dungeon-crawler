/*
Controls the enemy movement and shooting ai
By: Nick Petruccelli
Last Modified: 08/06/2023
*/

// (-) Did a little research, using System.Collections is redundant and can be removed the compiler knows this package.
using System.Collections;
using System.Collections.Generic;
// (-) Keep whats below
using UnityEngine;
using Pathfinding;

public class Enemy : MonoBehaviour
{
    
    // (-) Every single one of these public instance variables are named properly, Good Job!
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
    
    // (-) Every Private Variable needs to have a _ before the name, i.e: _damage, _player, _lastFireTime
    private float damage; 
    private Transform player;
    private float lastFireTime;
    private AIPath path;
    [SerializeField] private LayerMask layerMask;

    void Start()
    {
        // Locate the player gameObject
        player = GameObject.FindGameObjectWithTag("Player").transform;

        // Initializes shot reset timer
        lastFireTime = -fireRate;

        // Get A* Script
        path = gameObject.GetComponent<AIPath>();
    }

    void Update()
    {
        // Cast ray from enemy to player to see if wall is in between player and enemy
        
        // (-) This is inefficient, the reason is that the property of the component is used several times use a temp
        // (-) Variable such as _general_pos = transform.position
        // (-) When using a property it has to run computations to update that return type, unlike, a variable.
        // (-) I setup one of the transforms you swap it out and change the transform position too
        // (-) var player_pos = player.transform.position;
        
        RaycastHit2D ray = Physics2D.Raycast(transform.position, player.transform.position - transform.position, fireRange, layerMask);
        Debug.DrawRay(transform.position, player.transform.position - transform.position, Color.red);
        
        
        // (-) This is explicit comparison use this instead: collision.gameObject.CompareTag("Player")
        // If ray does not hit environment look at player and shoot.
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
    
    // Should be TakeDamage
    // Be careful with what names you choose for a class about taking "damage" maybe I'd suggest damageTaken
    public void takeDamage(float damage)
    {
        // (-) this can also be rewritten as
        // (-) hP -= damage;     OR If you dont like that       hP+=-(damage)
        
        hP = hP - damage;
        
        if(hP <= 0f)
        {
            Die();
        }
    }
    
    // (-) Add the modifier style, i.e. private
    void Die()
    {
        Instantiate(deathEffect, transform.position, Quaternion.identity);
        Destroy(gameObject);
    }
    
    // (-) Add the modifier style, i.e. private
    void Shoot()
    {
        GameObject bullet = Instantiate(bulletPreFab, firePoint.position, firePoint.rotation);
        Rigidbody2D rb = bullet.GetComponent<Rigidbody2D>();
        EnemyBullet bulletScript = bullet.GetComponent<EnemyBullet>();
        bulletScript.SetDamage(enemyDamage);
        rb.AddForce(firePoint.up * bulletForce, ForceMode2D.Impulse);
    }
    
    // (-) Add the modifier style, i.e. private
    void LookAtPlayer()
    {
        Vector2 lookDir = player.transform.position - transform.position;
        float angle = (Mathf.Atan2(lookDir.y, lookDir.x) * Mathf.Rad2Deg) - rotationOffSet;
        Quaternion q = Quaternion.AngleAxis(angle, Vector3.forward);
        transform.rotation = Quaternion.Slerp(transform.rotation, q, Time.deltaTime * rotationSpeed);
    }
}
