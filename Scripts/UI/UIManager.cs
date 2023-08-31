using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class UIManager : MonoBehaviour
{
    public PlayerNameUI playerNameUI;

    public void Start()
    {
        Debug.Log("UIStart");
        playerNameUI.ShowPlayerNames();
    }
}
