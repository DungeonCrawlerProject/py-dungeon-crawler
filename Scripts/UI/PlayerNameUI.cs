using System;
using Steamworks;
using UnityEngine;
using TMPro;

public class PlayerNameUI : MonoBehaviour
{
    public TMP_Text textMesh;
    public SteamManager steamManager;
    public const uint AppId = 460;

    public void ShowPlayerNames() {
        
        if (steamManager.lobbyPlayers.Count == 0) {

            if (!SteamClient.IsValid) {
                throw new Exception("Invalid SteamClient");
            }
            
            // Local 'my' player information
            textMesh.text = SteamClient.Name;
        }
        else {
            textMesh.text = steamManager.lobbyPlayers[0].Name;
        }
        
    }
}