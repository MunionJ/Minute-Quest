import pygame
from config import *

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

        self.rect = pygame.rect.Rect(self.pos.x, self.pos.y, 24, 24)
        self.debug = False
        self.states = ["standing", "jumping", "running", "falling"]
        self.cur_state = self.states[0]
        self.jump_offset = 0

    def move(self, keys, dt):
        """Base movement method."""
        # print(keys[pygame.K_s], keys[pygame.K_a], keys[pygame.K_d])
        movedHorizontal = False
        if keys[pygame.K_s]:
            # Implement ability to crouch?
            pass
        if keys[pygame.K_d]:
            if self.accel.x < MAX_X_ACC:
                self.accel.x += PLAYER_ACC
            movedHorizontal = True
        if keys[pygame.K_a]:
            if self.accel.x > -MAX_X_ACC:
                self.accel.x -= PLAYER_ACC
            movedHorizontal = True

        if keys[pygame.K_F1]:
            self.debug = not self.debug

        # if the entity is not currently moving, decrease their velocity until it reaches 0
        if movedHorizontal:
            self.cur_state = self.states[2]     # running
            self.prevPos = self.pos

            # self.velocity.length() returns the Euclidean length of the vector
            if self.velocity.length() > self.max_speed:
                self.velocity.scale_to_length(self.max_speed)

            self.pos += self.velocity
            self.rect.center = (int(self.pos.x), int(self.pos.y))

        if not keys[pygame.K_a]:
            if self.accel.x < 0:
                self.accel.x = 0
            if self.velocity.x < 0:
                self.velocity.x -= 2*PLAYER_FRICTION
                if self.velocity.x > 0:
                    self.velocity.x = 0
        if not keys[pygame.K_d]:
            if self.accel.x > 0:
                self.accel.x = 0
            if self.velocity.x > 0:
                self.velocity.x += 2*PLAYER_FRICTION
                if self.velocity.x < 0:
                    self.velocity.x = 0

    def update(self, keys, dt):
        """Base update method. Will be filled
            out later."""
        # Gravity and Player Movement

        # PLAYER JUMPING
        # TODO Update code to apply this if statement to check for all tiles rather than the bottom of the screen.
        self.apply_physics()

        self.velocity += self.accel * dt
        self.pos += self.velocity
        self.rect.center = self.pos
        self.move(keys, dt)

    def apply_physics(self):
        """ Apply physics based on Actor's current state."""
        if self.rect.bottom < SCREEN_RES[1] - 30:   # If pos is larger than 30 px off the floor, set state to falling
            self.cur_state = self.states[3]

        if self.cur_state == self.states[0]:   # If current state is standing, do not apply gravity
            self.accel = vec(0, 0)

        if self.cur_state == self.states[1]:   # If current state is jumping, add the jump vector
            self.velocity += self.jump_vector

        if self.cur_state == self.states[3]:   # If current state is falling, apply gravity
            self.accel += vec(0, PLAYER_GRAV)

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
