using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class UIManager : MonoBehaviour
{
    public PlayerNameUI playerNameUI;
    public GameObject escMenu;

    public void Start()
    {
        Debug.Log("UIStart");
        playerNameUI.ShowPlayerNames();
    }

    public void Update()
    {
        // check to see if esc is pressed and open or close it
        if (Input.GetKeyDown(KeyCode.Escape) )
        {
            escMenu.SetActive(!escMenu.activeSelf);
        }
    }
}
