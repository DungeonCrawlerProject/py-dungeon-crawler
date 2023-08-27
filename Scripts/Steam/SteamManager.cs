// The Manager that oversees all Steam functionality
// Uses SteamAPI Version: 1.0.13
// By: Sean McClanahan
// Last Modified: 08/18/2023
// Documentation: https://steamworks.github.io/installation/


using Steamworks;
using Steamworks.Data;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using UnityEngine;

public class SteamManager : MonoBehaviour {
    
    public static SteamManager Instance;
    private const uint AppId = 480;
    public static string PlayerName;
    public static SteamId PlayerId;
    public static string PlayerStringId;
    public bool hasConnectionToSteam;

    public List<Lobby> ActiveLobbies;
    
    private Lobby _hostedMultiplayerLobby;
    public Lobby CurrentLobby;
    
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

            hasConnectionToSteam = true;
        }
        catch {
            hasConnectionToSteam = false;
            PlayerStringId = "NoSteamId";
        }
        
    }


    void Start() {
        // SteamMatchmaking.OnLobbyGameCreated += OnLobbyGameCreatedCallback;
        // SteamMatchmaking.OnLobbyCreated += OnLobbyCreatedCallback;
        // SteamMatchmaking.OnLobbyEntered += OnLobbyEnteredCallback;
        SteamMatchmaking.OnLobbyMemberJoined += OnLobbyMemberJoinedCallback;
        // SteamMatchmaking.OnChatMessage += OnChatMessageCallback;
        SteamMatchmaking.OnLobbyMemberDisconnected += OnLobbyMemberDisconnectedCallback;
        SteamMatchmaking.OnLobbyMemberLeave += OnLobbyMemberLeaveCallback;
        // SteamFriends.OnGameLobbyJoinRequested += OnGameLobbyJoinRequestedCallback;
        // SteamApps.OnDlcInstalled += OnDlcInstalledCallback;
        // SceneManager.sceneLoaded += OnSceneLoaded;
    }

    void Update()
    {
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
            
            CurrentLobby = _hostedMultiplayerLobby;
            
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
    
    private void OtherLobbyMemberLeft(Friend friend) {
        if (friend.Id != PlayerId) {
            Debug.Log("Opponent has left the lobby");
            
            try {
                SteamNetworking.CloseP2PSessionWithUser(friend.Id);
                // Handle game / UI changes that need to happen when other player leaves
            }
            catch {
                Debug.Log("Unable to update disconnected player nameplate / process disconnect cleanly");
            }

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
    
    void OnLobbyMemberJoinedCallback(Lobby lobby, Friend friend) {
        Debug.Log("someone else joined lobby");
        if (friend.Id != PlayerId) {
            SteamNetworking.AcceptP2PSessionWithUser(friend.Id);
        }
    } 
}
