// A "DataClass" For containing information regarding a single player
// By: Sean McClanahan
// Last Modified: 08/31/2023

using Steamworks;


/// <summary>Stores Steam Player Information</summary>
public class LobbyPlayer {
    
    public SteamId Id;
    public string Name;
    
    public LobbyPlayer(SteamId id, string name) {
        Id = id;
        Name = name;
    }
}
