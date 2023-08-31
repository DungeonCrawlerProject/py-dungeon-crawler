using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class EnemySpawner : MonoBehaviour
{
    public List<GameObject> enemySpawns;

    private void OnTriggerEnter2D(Collider2D collision)
    {
        if (collision.tag == "Player")
        {
            GetComponent<BoxCollider2D>().enabled = !GetComponent<BoxCollider2D>().enabled;
            foreach (GameObject spawner in enemySpawns)
            {
                spawner.GetComponent<EnemySpawn>().Spawn();
            }
        }
    }

    /*
    private void OnCollisionEnter2D(Collision2D collision)
    {
        Debug.Log("Entered Room");
        foreach (GameObject spawner in enemySpawns)
        {
            spawner.GetComponent<EnemySpawn>().Spawn();
            Destroy(spawner);
        }
    }
    */
}
