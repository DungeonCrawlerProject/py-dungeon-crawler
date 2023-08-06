/*
Contains all of the logic for playing shooting using the Bullet class
By: Nick Petruccelli
Last Modified: 08/06/2023
*/

using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Bullet : MonoBehaviour
{

    public GameObject hitEffect;
    public float damage;

    void OnCollisionEnter2D(Collision2D collision)
    {
        if(collision.gameObject.tag == "Enemy")
        {
            Enemy enemyStats = collision.gameObject.GetComponent<Enemy>();
            enemyStats.takeDamage(damage);
        }

        Instantiate(hitEffect, transform.position, Quaternion.identity);
        Destroy(gameObject);
    }

    public void setDamage(float dam)
    {
        damage = dam;
    }
}
