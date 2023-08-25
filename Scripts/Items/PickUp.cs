/*
Script that allows player to pick up items off the ground currently only weapons but later all items
By: Nick Petruccelli
Last Modified: 08/10/2023
*/
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

    private void Start()
    {
        player = GameObject.FindGameObjectWithTag("Player").transform;
        
    }
    private void Update()
    {
        var itemPosition = transform.position;
        RaycastHit2D ray = Physics2D.Raycast(itemPosition, player.transform.position - itemPosition);

        if (ray.distance <= pickUpRange && Input.GetKeyDown(KeyCode.R))
        {
            switch (itemType)
            {
                case "Weapon":
                    // Drop equipped item on ground and remove it from player
                    RangedWeapon itemInfo = player.GetChild(0).GetComponent<RangedWeapon>();
                    Instantiate(itemInfo.groundItem, transform.position, Quaternion.identity, null);
                    Destroy(player.GetChild(0).gameObject);
                    
                    // Add new weapon to player and destroy ground object
                    float playerRotation = player.transform.rotation.eulerAngles.z;
                    playerRotation = playerRotation * Mathf.PI / 180;
                    Vector3 offSetAdjusted = new Vector3(-Mathf.Sin((playerRotation)), Mathf.Cos(playerRotation), 0f);
                    Weapon weapon = item.GetComponent<Weapon>();
                    offSetAdjusted = offSetAdjusted * weapon.pickUpOffSet;
                    var playerTransform = player.transform;
                    Instantiate(item, playerTransform.position + offSetAdjusted, playerTransform.rotation, playerTransform);
                    Destroy(gameObject);
                    break;

                case "Passive":
                    // Add items stats to playerStats
                    Item itemStats = item.GetComponent<Item>();
                    PlayerStats playerStats = player.GetComponent<PlayerStats>();
                    Weapon weaponEquipped = player.GetChild(0).GetComponent<Weapon>();
                    playerStats.maxHealth += itemStats.healthIncStatic;
                    playerStats.curHealth += itemStats.healthIncStatic;
                    playerStats.maxHealth *=  itemStats.healthIncMult;
                    weaponEquipped.damage += itemStats.damageIncStatic;
                    playerStats.damageMult += itemStats.damageIncMult;
                    playerStats.critChance += itemStats.critChanceIncStatic;

                    // Add item to inventory
                    playerStats.equippedItems.Add(itemStats.itemName);

                    Destroy(gameObject);
                    break;
            }
        }
    }
}
