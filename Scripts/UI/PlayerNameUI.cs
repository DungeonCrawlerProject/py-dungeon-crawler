using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class PlayerNameUI : MonoBehaviour
{
    public TMP_Text textMesh;
    public SteamManager steamManager;

    public void ShowPlayerNames()
    {
        Debug.Log("Name");
        List<String> playerNames = steamManager.GetPlayerNames();
        Debug.Log(playerNames);
        textMesh.text = playerNames[0];
    }
}