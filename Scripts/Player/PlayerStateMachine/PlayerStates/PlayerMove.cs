using UnityEngine;

public class PlayerMove : IPlayerState
{
    /// <summary>Determines if player state needs to change states and calls Move method</summary>
    /// <param name="player">Instance of player class</param>
    /// <returns>Returns IPlayerState interface</returns>
    public IPlayerState DoState(Player player)
    {
        Move(player);
        if (Input.GetKey(KeyCode.Space) && player.nextDodge < Time.time)
            return player.playerDodge;
        if (Input.GetAxisRaw("Horizontal") != 0 || Input.GetAxisRaw("Vertical") != 0)
            return player.playerMove;
        return player.playerIdle;
    }

    /// <summary>
    /// Gets direction that player needs to move from keyboard inputs
    /// </summary>
    /// <param name="player">Instance of player class</param>
    private void Move(Player player)
    {
        player.moveDirection.x = Input.GetAxisRaw("Horizontal");
        player.moveDirection.y = Input.GetAxisRaw("Vertical");
        
        player.moveDirection.Normalize();
    }
}
