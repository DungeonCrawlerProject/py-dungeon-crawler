using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class EnemySpawn : MonoBehaviour
{
    public GameObject enemy;
    public ParticleSystem enemySpawnParticles;

    public void Spawn()
    {
        StartCoroutine(Spawning());
    }

    IEnumerator Spawning()
    {
        // Play spawning in anim wher enemy will spawn
        Instantiate(enemySpawnParticles, transform.position, Quaternion.identity);
        yield return new WaitForSeconds(1);

        // Spawn Enemy
        Instantiate(enemy, transform.position, Quaternion.identity);
        Destroy(this.gameObject);
    }
}
