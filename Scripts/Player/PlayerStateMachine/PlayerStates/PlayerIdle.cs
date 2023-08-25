using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class PlayerIdle : IPlayerState
{
    public IPlayerState DoState(Player player)
    {
        if (Input.GetKey(KeyCode.Space) && player.nextDodge < Time.time)
            return player.playerDodge;
        if (Input.GetAxisRaw("Horizontal") != 0 || Input.GetAxisRaw("Vertical") != 0)
            return player.playerMove;
        return player.playerIdle;
    }

    public void Idle()
    {
        // Find where player needs to look
        
        // Play animation that corresponds to look direction
        
    }

    public void Move()
    {
        
    }
    
}
