using System.Collections;
using System.Collections.Generic;
using Unity.VisualScripting;
using UnityEngine;

public class PlayerMove : IPlayerState
{
    public IPlayerState DoState(Player player)
    {
        Move(player);
        if (Input.GetKey(KeyCode.Space) && player.nextDodge < Time.time)
            return player.playerDodge;
        if (Input.GetAxisRaw("Horizontal") != 0 || Input.GetAxisRaw("Vertical") != 0)
            return player.playerMove;
        return player.playerIdle;
    }

    private void Move(Player player)
    {
        player.moveDirection.x = Input.GetAxisRaw("Horizontal");
        player.moveDirection.y = Input.GetAxisRaw("Vertical");
        
        player.moveDirection.Normalize();
    }
}
