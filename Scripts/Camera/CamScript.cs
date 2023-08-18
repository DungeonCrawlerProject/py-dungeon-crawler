using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CamScript : MonoBehaviour
{
    public Transform target;
    public float damping = .5f;
    public Vector3 offSet = new Vector3(0f, 0f, -10f);

    private Vector3 velocity = Vector3.zero;

    void FixedUpdate()
    {
        Vector3 camTarget = target.position + offSet;
        transform.position = Vector3.SmoothDamp(transform.position, camTarget, ref velocity, damping);
    }
}
