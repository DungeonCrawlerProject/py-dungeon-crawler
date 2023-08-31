// The Manager that oversees all Steam functionality
// By: Sean McClanahan
// Last Modified: 08/18/2023
// Documentation: https://wiki.facepunch.com/steamworks/

using Steamworks;
using Steamworks.Data;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using UnityEngine;
using UnityEngine.Rendering;

public class SteamManager : MonoBehaviour {
    
    // Values that will never change and must remain constant during run-time.
    private const uint AppId = 480;
    
    public static SteamManager Instance;
    
    // Local Player Specific Variables
    public static string PlayerName;
    public static SteamId PlayerId;
    public static string PlayerStringId;
    
    // List of External 
    public List<SteamId> FriendSteamIds = new List<SteamId>();
    public List<String> FriendSteamNames = new List<string>();
    public List<Lobby> ActiveLobbies;
    
    private Lobby _hostedMultiplayerLobby;
    private Lobby _currentLobby;
    
    public bool applicationHasQuit;
    
    private void Awake() {
        if (Instance != null) {
            Debug.Log("The Instance Already Exists");
            return;
        }

        Instance = this;
        DontDestroyOnLoad(this);
        
        try {
            SteamClient.Init(AppId, asyncCallbacks: true);

            if (!SteamClient.IsValid) {
                throw new Exception("Invalid SteamClient");
            }

            // Local 'my' player information
            PlayerName = SteamClient.Name;

            PlayerId = SteamClient.SteamId;
            PlayerStringId = SteamClient.SteamId.ToString();
        }
        catch {
            PlayerStringId = "NoSteamId";
        }
    }


    void Start() {
        // SteamMatchmaking.OnLobbyGameCreated += OnLobbyGameCreatedCallback;
        // SteamMatchmaking.OnLobbyCreated += OnLobbyCreatedCallback;
        // SteamMatchmaking.OnLobbyEntered += OnLobbyEnteredCallback;
        // SteamMatchmaking.OnChatMessage += OnChatMessageCallback;
        SteamMatchmaking.OnLobbyMemberJoined += OnLobbyMemberJoinedCallback;
        SteamMatchmaking.OnLobbyMemberDisconnected += OnLobbyMemberDisconnectedCallback;
        SteamMatchmaking.OnLobbyMemberLeave += OnLobbyMemberLeaveCallback;
        // SteamFriends.OnGameLobbyJoinRequested += OnGameLobbyJoinRequestedCallback;
        // SteamApps.OnDlcInstalled += OnDlcInstalledCallback;
        // SceneManager.sceneLoaded += OnSceneLoaded;
        CreateLobby(0);
        
    }

    void Update() {
        SteamClient.RunCallbacks();
    }

    private void OnApplicationQuit() {
        try {
            SteamClient.Shutdown();
        } catch {
            Debug.Log("Steamworks was unable to shutdown properly.");
        }
    }
    
    
    public async Task<bool> CreateLobby(int lobbyParameters, int maxPlayers = 4) {
        try {
            var createLobbyOutput = await SteamMatchmaking.CreateLobbyAsync(maxMembers: maxPlayers);
            
            if (!createLobbyOutput.HasValue) {
                throw new Exception("Lobby created but not correctly instantiated");
            }
            
            _hostedMultiplayerLobby = createLobbyOutput.Value;
            _hostedMultiplayerLobby.SetPublic();
            _hostedMultiplayerLobby.SetJoinable(true);
            // hostedMultiplayerLobby.SetData(staticDataString, lobbyParameters.ToString());
            
            _currentLobby = _hostedMultiplayerLobby;
            SteamFriends.OpenGameInviteOverlay(_currentLobby.Id);
            return true;
        }
        catch (Exception exception) {
            Debug.Log(exception.ToString());
            return false;
        }
    } 
    
    void OnLobbyMemberDisconnectedCallback(Lobby lobby, Friend friend) {
        OtherLobbyMemberLeft(friend);
    }

    void OnLobbyMemberLeaveCallback(Lobby lobby, Friend friend) {
        OtherLobbyMemberLeft(friend);
    }
    
    void OnLobbyMemberJoinedCallback(Lobby lobby, Friend friend) {
        OtherLobbyMemberJoin(friend);
    } 
    
    private void OtherLobbyMemberJoin(Friend friend) {
        
        Debug.Log("Trying to establish new connection with " + friend.Name);
        
        if (friend.Id == PlayerId) {
            
        }

        try
        {
            // --------------Handle game / UI changes that need to happen when other player leaves----------------------
            SteamNetworking.AcceptP2PSessionWithUser(friend.Id);
            FriendSteamIds.Add(friend.Id);
            FriendSteamNames.Add(friend.Name);
            Debug.Log("Establish connection with " + friend.Name);
        }
        catch (Exception e){
            Debug.Log("Unable to update connected player nameplate / process connect cleanly " + e);
        }
    }
    
    private void OtherLobbyMemberLeft(Friend friend) {
        
        // Skip if it is the local player
        if (friend.Id != PlayerId) {
            return;
        }
        
        Debug.Log("Opponent has left the lobby");
        
        try {
            // --------------Handle game / UI changes that need to happen when other player leaves----------------------
            SteamNetworking.CloseP2PSessionWithUser(friend.Id);
            
            // Remove the player Id from the list if that Id exists
            if (FriendSteamIds.Contains(friend.Id)) {
                FriendSteamIds.Remove(friend.Id);
                Debug.Log(friend.Name +  " Has left the server");
            }
        }
        catch {
            Debug.Log("Unable to update disconnected player nameplate / process disconnect cleanly");
        }
        
    }
    
    /// <summary> Clears the Active Lobbies and repopulates them with the SteamLobbyList with 20 max results </summary>
    public async Task RefreshMultiplayerLobbies() {
        try {
            ActiveLobbies.Clear();
            // Lobby[] lobbies = await SteamMatchmaking.LobbyList.WithMaxResults(20).WithKeyValue(isRankedDataString, FALSE).RequestAsync();
            
            var lobbies = await SteamMatchmaking.LobbyList.WithMaxResults(20).RequestAsync();
            
            // The No need to look for multiplayer lobbies if there are none.
            if (lobbies == null) {
                return;
            }
            
            foreach (var lobby in lobbies.ToList()) {
                ActiveLobbies.Add(lobby);
            }
        }
        catch (Exception e) {
            Debug.Log("Error fetching multiplayer lobbies "+ e);
        }
    }

    public List<String> GetPlayerNames()
    {
        var result = new List<String>();
        result.Add(PlayerName);
        foreach (var _playerName in FriendSteamNames)
        {
            
            result.Add(_playerName);
        }

        if (result.Count > 4)
        {
            throw new Exception("Overload Player Count");
        }

        return result;
    }
}
