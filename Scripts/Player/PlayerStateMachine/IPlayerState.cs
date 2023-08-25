using System.Collections;
using System.Collections.Generic;
using UnityEditor.IMGUI.Controls;
using UnityEngine;

public interface IPlayerState
{
    IPlayerState DoState(Player player);
}
