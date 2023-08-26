using UnityEngine;


public class PlayerDodge : IPlayerState
{
    private float dodgeStartTime = 10f;
    private bool canDodge = true;
    /// <summary>Determines if player state needs to change states and calls Dodge method</summary>
    /// <param name="player">Instance of player class</param>
    /// <returns>Returns IPlayerState interface</returns>
    public IPlayerState DoState(Player player)
    {
        Dodge(player);
        if (player.dodgeDuration > Time.time - dodgeStartTime)
            return player.playerDodge;
        if (Input.GetAxisRaw("Horizontal") != 0 || Input.GetAxisRaw("Vertical") != 0)
            return player.playerMove;
        return player.playerIdle;
    }

    /// <summary>Moves the player in a fixed direction at a faster speed</summary>
    /// <param name="player">Instance of player class</param>
    private void Dodge(Player player)
    {
        if (canDodge)
        {
            player.moveDirection.x = Input.GetAxisRaw("Horizontal");
            player.moveDirection.y = Input.GetAxisRaw("Vertical");
        
            player.moveDirection.Normalize();

            dodgeStartTime = Time.time;
            player.nextDodge = Time.time + player.dodgeDelay;
            canDodge = false;
        }

        if (player.nextDodge < Time.time)
        {
            canDodge = true;
        }
    }
}
