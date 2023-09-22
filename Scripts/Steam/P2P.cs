// The P2P Packet Manager
// By: Sean McClanahan
// Last Modified: 08/31/2023


using Steamworks;
using UnityEngine;

public class P2P : MonoBehaviour {

    private void Awake() {
        InvokeRepeating(nameof(ReceiveDataPacket), 0f, 0.05f);
    }
    
    /// <summary>Boiler Plate for where to handle receiving Data Packet</summary>
    public void ReceiveDataPacket() {
        while (SteamNetworking.IsP2PPacketAvailable()) {
            
            var packet = SteamNetworking.ReadP2PPacket();
            
            if (packet.HasValue) {
                HandleFriendDataPacket(packet.Value.Data);
            }
        }
    }
    
    /// <summary> Sends a dataString Packet to all of the other players </summary>
    /// <param name="dataString"> The adHocData Data-string. </param>
    /// <param name="attempts"> How many times it should try to send the packet.</param>
    public void SendPacket(string dataString, int attempts = 2) {
        
        // Get each playerId
        foreach (var _player in SteamManager.Instance.lobbyPlayers) {
            // Try to run it twice. If the first time it works return
            for (int i = 0; i < attempts; i++) {
                var sentSuccessfully = SteamNetworking.SendP2PPacket(
                    steamid: _player.Id,
                    data: System.Text.Encoding.UTF8.GetBytes(dataString)
                );
                if (sentSuccessfully) {}
            }
        }
    }
    
    private void HandleFriendDataPacket(byte[] dataPacket) {
        try {
            // Do P2P Packet Here
            string opponentDataSent = System.Text.Encoding.UTF8.GetString(dataPacket);
            
        }
        catch {
            Debug.Log("Failed to process incoming opponent data packet");
        }
    }
}