from dataclasses import dataclass


@dataclass
class Position:
    x: float
    y: float

@dataclass
class Player:
    position: Position
    speed: float
    sprint_factor: float = 1.5



#     _currentState;
#     playerIdle = new PlayerIdle();
#     playerMove = new PlayerMove();
#     playerDodge = new PlayerDodge();
#
#     public Vector2 moveDirection;
#     public float moveSpeed = 10;
#     public float dodgeSpeed = 20;
#
#     public float dodgeDelay = 1f;
#     public float nextDodge;
#     public float dodgeDuration = .25f;
#
#     public Rigidbody2D rb;
#     public Camera cam;
#
#     private Vector2 mousePos;
#
#     private void Start()
#     {
#         currentState = playerIdle;
#     }
#
#     private void Update()
#     {
#         currentState = currentState.DoState(this);
#
#         // Gets mouse position
#         mousePos = cam.ScreenToWorldPoint(Input.mousePosition);
#     }
#
#
#     private void FixedUpdate()
#     {
#         // move player according to state
#         if (currentState == playerMove)
#         {
#             rb.MovePosition(rb.position + (moveSpeed * Time.fixedDeltaTime) * moveDirection);
#         }
#         if (currentState == playerDodge)
#         {
#             rb.MovePosition(rb.position + (dodgeSpeed * Time.fixedDeltaTime) * moveDirection);
#         }
#
#         // Makes Player Look At Mouse: temporary until i set up weapon system
#         Vector2 lookDir = mousePos - rb.position;
#         float angle = (Mathf.Atan2(lookDir.y, lookDir.x) * Mathf.Rad2Deg)-90;
#         rb.rotation = angle;
#     }
# }
