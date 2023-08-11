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


    private Transform player;

    /*
    enum PickUpType
    {
        Weapon,
        Passive
    }
   */

    void Start()
    {
        player = GameObject.FindGameObjectWithTag("Player").transform;
        
    }
    void Update()
    {
        RaycastHit2D ray = Physics2D.Raycast(transform.position, player.transform.position - transform.position);

        if (ray.distance <= pickUpRange && Input.GetKeyDown(KeyCode.R) == true)
        {
            switch (itemType)
            {
                case "Weapon":
                    // Drop equiped item on ground and remove it from player
                    RangedWeapon itemInfo = player.GetChild(0).GetComponent<RangedWeapon>();
                    Instantiate(itemInfo.groundItem, transform.position, Quaternion.identity, null);
                    Destroy(player.GetChild(0).gameObject);

                    // Add new wepon to player and destroy ground object
                    float playerRotation = player.transform.rotation.eulerAngles.z;
                    playerRotation = playerRotation * Mathf.PI / 180;
                    Vector3 offSetAdjusted = new Vector3(-Mathf.Sin((playerRotation)), Mathf.Cos(playerRotation), 0f);
                    Weapon weapon = item.GetComponent<Weapon>();
                    offSetAdjusted = offSetAdjusted * weapon.pickUpOffSet;
                    Instantiate(item, player.transform.position + offSetAdjusted, player.transform.rotation, player.transform);
                    Destroy(gameObject);
                    break;

                case "Passive":
                    // Add items stats to playerStats
                    Item itemStats = item.GetComponent<Item>();
                    PlayerStats playerStats = player.GetComponent<PlayerStats>();
                    Weapon weaponEqpd = player.GetChild(0).GetComponent<Weapon>();
                    playerStats.maxHealth += itemStats.healthIncStatic;
                    playerStats.curHealth += itemStats.healthIncStatic;
                    playerStats.maxHealth *=  itemStats.healthIncMult;
                    weaponEqpd.damage += itemStats.damageIncStatic;
                    playerStats.damageMult += itemStats.damageIncMult;
                    playerStats.critChance += itemStats.critChanceIncStatic;

                    // Add item to inventory
                    playerStats.equipedItems.Add(itemStats.itemName);
                    break;
            }
        }
    }
}
