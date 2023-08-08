/*
Controls player movment
By: Nick Petruccelli
Last Modified: 08/06/2023
*/

using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerMovment : MonoBehaviour
{

    public float moveSpeed = 5f;
    public Rigidbody2D rb;
    Vector2 movment;

    public Camera cam;
    Vector2 mousePos;


    // Update is called once per frame
    void Update()
    {
        // Movment
        movment.x = Input.GetAxisRaw("Horizontal");
        movment.y = Input.GetAxisRaw("Vertical");
        movment.Normalize();

        // Look Direction
        mousePos = cam.ScreenToWorldPoint(Input.mousePosition);
    }

    void FixedUpdate()
    {
        // Moves Player
        rb.MovePosition(rb.position + movment * moveSpeed * Time.fixedDeltaTime);

        // Makes Player Look At Mouse
        Vector2 lookDir = mousePos - rb.position;
        float angle = (Mathf.Atan2(lookDir.y, lookDir.x) * Mathf.Rad2Deg)-90;
        rb.rotation = angle;
    }
}
