using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PickUp : MonoBehaviour
{
    public string itemType;
    public GameObject item;
    public float pickUpRange = 10;
    public Vector3 offSet;

    private Transform player;

    void Start()
    {
        player = GameObject.FindGameObjectWithTag("Player").transform;
    }
    void Update()
    {
        RaycastHit2D ray = Physics2D.Raycast(transform.position, player.transform.position - transform.position);

        if (ray.distance <= pickUpRange && (Input.GetKeyDown(KeyCode.R) == true))
        {
            Instantiate(player.GetChild(0), transform.position, Quaternion.identity, null);
            Destroy(player.GetChild(0).gameObject);
            Instantiate(item, player.transform.position + offSet, player.transform.rotation, player.transform);
            Destroy(gameObject);
        }
    }
}
