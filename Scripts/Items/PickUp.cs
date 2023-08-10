/*
Script that allows player to pick up items off the ground currently only weapons but later all items
By: Nick Petruccelli
Last Modified: 08/10/2023
*/
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PickUp : MonoBehaviour
{
    public string itemType;
    public GameObject item;
    public float pickUpRange = 10;
    public float offSet;

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
            // Drop equiped item on ground and remove it from player
            RangedWeapon itemInfo = player.GetChild(0).GetComponent<RangedWeapon>();
            Instantiate(itemInfo.groundItem, transform.position, Quaternion.identity, null);
            Destroy(player.GetChild(0).gameObject);

            // Add new wepon to player and destroy ground object
            float playerRotation = player.transform.rotation.eulerAngles.z;
            playerRotation = playerRotation * Mathf.PI / 180;
            Vector3 offSetAdjusted = new Vector3 (-Mathf.Sin((playerRotation)), Mathf.Cos(playerRotation), 0f);
            offSetAdjusted = offSetAdjusted * offSet;
            Debug.Log(playerRotation);
            Debug.Log(offSetAdjusted);
            Instantiate(item, player.transform.position + offSetAdjusted, player.transform.rotation, player.transform);
            Destroy(gameObject);
        }
    }
}
