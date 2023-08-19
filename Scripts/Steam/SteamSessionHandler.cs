/*
 * The Handler that Controls the Multiplayer Sessions (*Currently Only Logs SOLO player's Steam Username)
 * By: Sean McClanahan
 * Last Modified: 08/18/2023
 */


using UnityEngine;
using Steamworks;
using System.Collections.Generic;

public class SteamSessionHandler : MonoBehaviour {

    public string user_name = "";
    public List<string> names = new List<string>();
    
    void Start() {
        if(SteamManager.Initialized) {
            user_name = SteamFriends.GetPersonaName();
            names.Add(user_name);
            Debug.Log(name);
        }
    }
}
