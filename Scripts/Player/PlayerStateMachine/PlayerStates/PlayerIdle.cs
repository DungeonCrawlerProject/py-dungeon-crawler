using UnityEngine;

public class PlayerIdle : IPlayerState
{
    /// <summary>Determines if player state needs to change states and calls Idle method</summary>
    /// <param name="player">Instance of player class</param>
    /// <returns>Returns IPlayerState interface</returns>
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
        // ToDo: Play animation that corresponds to look direction
    }
}
