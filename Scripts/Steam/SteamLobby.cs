// The Steam Lobby Manager will update gui based on who is in the lobby
// By: Sean McClanahan
// Last Modified: 08/27/2023

using System.Collections.Generic;
using Steamworks;
using UnityEngine;
using TMPro;

public class SteamLobby : MonoBehaviour {

    public TMP_Text player1Text;
    public TMP_Text player2Text;
    public TMP_Text player3Text;
    public TMP_Text player4Text;
    public List<string> _playerNames;
    private List<TMP_Text> _textNames;
    public int playerNumMemory;
    
    public SteamManager steamManager;
    
    // Start is called before the first frame update
    private void Start() {
        _textNames = new List<TMP_Text> {
            player1Text,
            player2Text,
            player3Text,
            player4Text
        };
        _playerNames = steamManager.GetPlayerNames();
        RefreshLobbyNames();
        steamManager.CreateLobby(2);
    }
    
    // Update is called once per frame
    private void Update() {
        _playerNames = steamManager.GetPlayerNames();

        // If and only if the numbers of players change, then we refresh the lobby names
        if (playerNumMemory != _playerNames.Count) {
            RefreshLobbyNames();
        }
        
    }
    
    
    /// <summary>Will call from the SteamManager and receive the playerNames and add the name to the lobby.</summary>
    private void RefreshLobbyNames(int maxPlayers = 4) {
        
        
        //TODO Check contents
        try {
            var hi = _playerNames;
        }
        catch {
            return;
        }
        
        // Run through used players and updates if.
        for (int i = 0; i < _playerNames.Count; i++) {
            _textNames[i].text = _playerNames[i];
            _textNames[i].color = Color.green;
        }

        // Runs through not used players and updates if the player leaves
        for (int i = _playerNames.Count; i < maxPlayers; i++) {
            _textNames[i].text = "Player" + (i + 1);
            _textNames[i].color = Color.gray;
        }
        playerNumMemory = _playerNames.Count;
    }
}
