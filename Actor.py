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
        self.rect = None
        self.debug = True
        self.states = ["standing", "jumping", "running", "falling"]
        self.cur_state = self.states[0]
        self.jump_offset = 0

    def move(self, keys, dt):
        """Base movement method."""
        pass

    def set_pos(self, new_rect):
        """ Sets the player's position."""
        if int(self.rect[0]) != int(new_rect[0]):
            self.rect[0] = new_rect[0]
            self.velocity.x = 0
            self.accel.x = 0
            self.pos.x = self.rect.center[0]
        if int(self.rect[1]) != int(new_rect[1]):
            self.rect[1] = new_rect[1]
            self.velocity.y = 0
            self.accel.y = 0
            self.pos.y = self.rect.center[1]

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
        if self.rect.bottom < SCREEN_RES[1] - 30:   # If pos is larger than 30 px off the floor, set state to falling
            self.cur_state = self.states[3]

        if self.cur_state == self.states[0]:   # If current state is standing, do not apply gravity
            self.accel = vec(0, 0)

        if self.cur_state == self.states[1]:   # If current state is jumping, add the jump vector
            self.velocity += self.jump_vector

        if self.cur_state == self.states[3]:   # If current state is falling, apply gravity
            self.accel += vec(0, PLAYER_GRAV)

        self.velocity += self.accel * dt
        self.pos += self.velocity
        self.rect.center = self.pos

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
