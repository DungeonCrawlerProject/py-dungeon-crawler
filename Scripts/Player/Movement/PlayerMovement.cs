/*
Controls player movement
By: Nick Petruccelli
Last Modified: 08/19/2023
*/

using UnityEngine;

public class PlayerMovement : MonoBehaviour {

    public float moveSpeed = 5f;
    public Rigidbody2D rb;
    private Vector2 _movement;

    public Camera cam;
    private Vector2 _mousePos;


    // Update is called once per frame
    void Update() {
        // Movement
        _movement.x = Input.GetAxisRaw("Horizontal");
        _movement.y = Input.GetAxisRaw("Vertical");
        
        _movement.Normalize();

        // Look Direction
        _mousePos = cam.ScreenToWorldPoint(Input.mousePosition);
    }

    void FixedUpdate() {
        // Moves Player
        float speedMultiplier = 1.0f;
        if (Input.GetKey(KeyCode.LeftShift)) {
            speedMultiplier = 1.5f;
        }
        
        // Multiplying a 3 scalars then 1 vector is faster than one vector by 3 separate scalars. 
        rb.MovePosition(rb.position +   (moveSpeed * speedMultiplier) * Time.fixedDeltaTime * _movement);
        
        // Makes Player Look At Mouse
        Vector2 lookDir = _mousePos - rb.position;
        float angle = (Mathf.Atan2(lookDir.y, lookDir.x) * Mathf.Rad2Deg)-90;
        rb.rotation = angle;
    }
}
