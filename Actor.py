import pygame
from config import *
from PlayerStates import PlayerStates as states
vec = pygame.math.Vector2


class Actor(pygame.sprite.Sprite):
    """This is the base class from which Player,
        Enemy, etc. will inherit from."""
    def __init__(self, start_pos):
        # CONSTRUCTOR PARAMETERS #
        # start_pos: a tuple containing a coordinate pair (x, y)
        # img: a .PNG file (a sprite sheet, ideally)

        super().__init__()
        self.pos = vec(start_pos[0], start_pos[1])
        self.prevPos = self.pos
        self.velocity = vec(0, 0)
        self.accel = vec(0, 0)
        self.jump_vector = vec(0, -JUMP_VEC)
        self.max_speed = 10
        self.rect = None
        self.debug = True
        self.cur_state = states.Falling
        self.jump_offset = 0
        self.onSurface = False

    def move(self, keys, dt):
        """Base movement method meant to be overriden."""
        pass

    def set_pos(self, new_rect):
        """ Sets the player's position."""
        if int(self.rect[0]) != int(new_rect[0]):
            self.rect[0] = new_rect[0]
            self.velocity.x = 0
            self.accel.x = 0
            self.pos.x = self.rect.center[0]

        if int(self.rect[1]) != int(new_rect[1]):
            dy = self.rect[1] - new_rect[1]
            self.rect[1] = new_rect[1]
            self.velocity.y = 0
            self.accel.y = 0
            self.pos.y = self.rect.center[1]


            self.onSurface = True

    def moveX(self):
        self.velocity.x += self.accel.x

        # self.velocity.length() returns the Euclidean length of the vector
        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

        self.pos.x += self.velocity.x
        self.rect.center = (int(self.pos.x), int(self.pos.y))

    def moveY(self):
        self.velocity.y += self.accel.y

        # self.velocity.length() returns the Euclidean length of the vector
        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

        self.pos.y += self.velocity.y
        self.rect.center = (int(self.pos.x), int(self.pos.y))

    def update(self, keys, dt):
        """Base update method. Will be filled
            out later."""
        # Gravity and Player Movement

        # PLAYER JUMPING
        # TODO Update code to apply this if statement to check for all tiles rather than the bottom of the screen.
        self.apply_physics(dt)
        self.move(keys, dt)

    def apply_physics(self, dt):
        """ Apply physics based on Actor's current state."""
        if self.cur_state == states.Standing:   # If current state is standing or running, do not apply gravity
            self.accel = vec(0, 0)

        if self.cur_state == states.Jumping:   # If current state is jumping, add the jump vector
            self.velocity += self.jump_vector

        if self.cur_state == states.Falling:   # If current state is falling, apply gravity
            self.accel += vec(0, PLAYER_GRAV)


    def determineState(self):
        if self.velocity.y > 0:
            self.changeState(states.Falling)

        if self.velocity.y < 0:
            self.changeState(states.Jumping)

        if self.cur_state != states.Jumping or self.cur_state != states.Falling:
            if self.velocity.x != 0:
                if self.cur_state != states.Running:
                    self.changeState(states.Running)
                else:
                    self.changeState(states.Standing)

        if self.velocity.x == 0 and self.velocity.y == 0 and self.onSurface:
            self.changeState(states.Standing)

        if not self.onSurface:
            self.changeState(states.Falling)


    def isInAir(self):
        self.onSurface = False

    def changeState(self, newState):

        if self.cur_state != newState:
            self.cur_state = newState
            if newState == states.Standing:  # standing
                self.accel.y = 0
            elif newState == states.Jumping:  # jumping
                pass
            elif newState == states.Running:  # running
                pass
            elif newState == states.Falling:  # falling
                self.accel.y += PLAYER_GRAV

    def handleXCollision(self,other_rect):
        if self.velocity.x > 0:
            if self.rect.left < other_rect.right:
                self.rect.right = other_rect.left
                self.hitVerticalWall()
        elif self.velocity.x < 0:
            if self.rect.right > other_rect.left:
                self.rect.left = other_rect.right
                self.hitVerticalWall()

    def handleYCollision(self,other_rect):
        if self.velocity.y > 0:
            if self.rect.top < other_rect.bottom:
                self.rect.bottom = other_rect.top
                self.accel.y = 0
                self.velocity.y = 0
                self.pos.y = self.rect.center[1]
                self.onSurface = True
        elif self.velocity.y < 0:
            if self.rect.bottom > other_rect.top:
                self.accel.y = 0
                self.velocity.y = 0
                self.pos.y = self.rect.center[1]
        else:
            if self.rect.bottom != other_rect.top:
                self.rect.bottom = other_rect.top
                self.accel.y = 0
                self.velocity.y = 0
                self.pos.y = self.rect.center[1]


    def hitVerticalWall(self):
        self.accel.x = 0
        self.velocity.x = 0
        self.pos.x = self.rect.center[0]

    def draw(self, window):
        """Base draw method. Will be filled
            out later."""
        # temporarily just drawing a rect
        pygame.draw.rect(window,
                         (255, 255, 255),
                         self.rect
                         )
        if self.debug:
            pygame.draw.rect(window,
                             (255, 0, 0),
                             self.rect,
                             2)
