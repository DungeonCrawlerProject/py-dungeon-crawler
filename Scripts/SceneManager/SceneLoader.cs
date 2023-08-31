using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class SceneLoader : MonoBehaviour
{
    public void EnterSinglePlayer()
    {
        SceneManager.LoadScene(1);
    }

    public void EnterMultiPlayer()
    {
        SceneManager.LoadScene(1);
    }
    
    public void EnterMainMenu()
    {
        SceneManager.LoadScene(0);
    }

    public void QuitGame()
    {
        Application.Quit();
    }
}
