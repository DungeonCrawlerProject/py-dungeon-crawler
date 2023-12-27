from dataclasses import dataclass

from Scripts.Player.Movement.player_stats import PlayerStats
from Scripts.Player.PlayerStateMachine.PlayerStates.player_idle import PlayerIdle
from Scripts.Player.PlayerStateMachine.PlayerStates.player_move import PlayerMove
from Scripts.Player.PlayerStateMachine.PlayerStates.player_dodge import PlayerDodge
from Scripts.Player.PlayerStateMachine.player_state import IPlayerState


# TODO Position is temp
@dataclass
class Position:
    x: float
    y: float


@dataclass
class Player:
    position: Position
    stats: PlayerStats = PlayerStats()
    current_state: IPlayerState = PlayerMove

    def update(self) -> None:

        if self.current_state == PlayerMove:
            PlayerMove.move(self)

        if self.current_state == PlayerIdle:
            raise NotImplementedError

        if self.current_state == PlayerDodge:
            raise NotImplementedError

    def take_damage(self, damage: float):

        self.stats.current_health -= damage

        # healthBar.SetHealth(curHealth / maxHealth);

        if self.stats.current_health < 0:
            self.kill_player()

    def kill_player(self):
        raise NotImplementedError

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
