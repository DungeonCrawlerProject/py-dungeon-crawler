using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Enemy : MonoBehaviour
{

    public float hP = 20f;
    public float agroRange = 20f;
    public float fireRange=15f;
    public ParticleSystem deathEffect;

    private float damage;
    private Transform player;
    private Vector2 enemyOrigin;
    private Vector2 playerVec;

    void Start()
    {
        // Initilize player and enemyOrigin vectors
        player = GameObject.FindGameObjectWithTag("Player").transform;
        playerVec = new Vector2(player.transform.position.x, player.transform.position.y);
        enemyOrigin = new Vector2(gameObject.transform.position.x, gameObject.transform.position.y);


    }

    void Update()
    {
        // Update plyer and enemyOrigin vectors
        playerVec.x = player.transform.position.x;
        playerVec.y = player.transform.position.y;
        enemyOrigin.x = gameObject.transform.position.x;
        enemyOrigin.y = gameObject.transform.position.y;

        // Cast ray from enemy to player to see if wall is in between player and enemy
        Physics2D.Raycast(enemyOrigin, playerVec, fireRange);
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
        Destroy(transform.parent.gameObject);
    }
}
