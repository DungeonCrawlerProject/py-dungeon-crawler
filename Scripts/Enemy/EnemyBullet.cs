using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class EnemyBullet : MonoBehaviour
{
    public GameObject hitEffect;
    public float damage;
    
    // I would like to see a modifier, Slap on a private at the beginning
    void OnCollisionEnter2D(Collision2D collision)
    {
        // This is explicit comparison use this instead: collision.gameObject.CompareTag("Player")
        if (collision.gameObject.tag == "Player")
        {
            PlayerStats player = collision.gameObject.GetComponent<PlayerStats>();
            player.TakeDamage(damage);
        }

        Instantiate(hitEffect, transform.position, Quaternion.identity);
        Destroy(gameObject);
    }

    public void SetDamage(float dam)
    {
        damage = dam;
    }
}
