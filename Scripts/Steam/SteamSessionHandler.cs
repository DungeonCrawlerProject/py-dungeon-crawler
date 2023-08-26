/*
 * The Handler that Controls the Multiplayer Sessions (*Currently Only Logs SOLO player's Steam Username)
 * By: Sean McClanahan
 * Last Modified: 08/18/2023
 */


using UnityEngine;
using Steamworks;
using System.Collections.Generic;
using Unity.VisualScripting;
using UnityEngine.Serialization;


public class SteamSessionHandler : MonoBehaviour {

    [FormerlySerializedAs("userName")] [FormerlySerializedAs("user_name")] public string localUserName = "";
    public List<string> names = new List<string>();
    
    public HSteamListenSocket listenSocket;
    private Callback<P2PSessionRequest_t> p2pSessionRequestCallback;

    
    private void Start() {
        if (SteamManager.Initialized) {
            
            // Ill clean this later
            localUserName = SteamFriends.GetPersonaName();
            
            names.Add(localUserName);
            
            p2pSessionRequestCallback = Callback<P2PSessionRequest_t>.Create(OnP2PSessionRequest);
    
            // SteamMatchmaking.
            // SteamGameServer.
            // listenSocket = SteamGameServerNetworkingSockets.CreateListenSocketP2P(0, 0, null);
        }
    }

    private void OnP2PSessionRequest(P2PSessionRequest_t request)
    {
        // Accept the incoming P2P session request
        // SteamGameServerNetworkingSockets.AcceptP2PSessionWithUser(request.m_steamIDRemote);
        // SteamGameServerNetworkingSockets.AcceptP2PSessionWithUser()
        // You can now use the P2P connection with the remote user (request.m_steamIDRemote)
    }
    
    
    
    /// <summary>Returns a dictionary of string username key to int id</summary>
    /// <param name="annoyNick">Used to invite Nick to the game, doesn't work fully.</param>
    /// <returns>Dictionary</returns>
    private static Dictionary<string, int> GetFriendDict(bool annoyNick = false)
    {
        var friendsList = new Dictionary<string, int>();
            
        for (int i = 0; i < SteamFriends.GetFriendCount(EFriendFlags.k_EFriendFlagImmediate); i++)
        {
            var friendId = SteamFriends.GetFriendByIndex(i, EFriendFlags.k_EFriendFlagImmediate);
            var friendName = SteamFriends.GetFriendPersonaName(friendId);
                
            friendsList.Add(friendName, (int)friendId.m_SteamID);
            
            if (friendName == "Nick" && annoyNick)
            {
                SteamFriends.InviteUserToGame(friendId, "23asxzs8jsn99xhws9sueb");
            }
        }
        return friendsList;
    }
}
