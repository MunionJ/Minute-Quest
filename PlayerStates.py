from enum import Enum

class PlayerStates(Enum):
    Standing = 1
    Running = 2
    Jumping = 3
    Falling = 4
    Attacking = 5
    Dying = 6
    Damaged = 7