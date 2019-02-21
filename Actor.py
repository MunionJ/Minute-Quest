import pygame
from config import *

vec = pygame.math.Vector2


class Actor(pygame.sprite.Sprite):
    """This is the base class from which Player,
        Enemy, etc. will inherit from."""
    def __init__(self, start_pos, img):
        # CONSTRUCTOR PARAMETERS #
        # start_pos: a tuple containing a coordinate pair (x, y)
        # img: a .PNG file (a sprite sheet, ideally)

        super().__init__()
        self.pos = vec(start_pos[0], start_pos[1])
        self.prevPos = self.pos
        self.velocity = vec(0, 0)
        self.accel = vec(0.5, 0)
        self.jump_vector = vec(0.2, -4)
        self.max_speed = 10
        self.image = pygame.image.load(img)
        self.rect = pygame.rect.Rect(self.pos.x, self.pos.y, 24, 24)
        self.debug = False
        self.states = ["standing", "jumping", "running", "falling"]
        self.cur_state = self.states[0]
        self.jump_offset = 0

    # Possibly add the movement code to the player class specifically, as we will not be controlling enemies with key
    #  presses, they will have their own unique movement
    def move(self, keys, dt):
        """Base movement method."""
        # print(keys[pygame.K_s], keys[pygame.K_a], keys[pygame.K_d])
        movedHorizontal = False
        if keys[pygame.K_s]:
            # Implement ability to crouch?
            pass
        if keys[pygame.K_d]:
            self.velocity.x += self.accel.x * dt
            movedHorizontal = True
        if keys[pygame.K_a]:
            self.velocity.x -= (self.accel.x * dt)
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

        if not movedHorizontal:
            self.velocity.x /= 10
            if abs(self.velocity.x) < 0.1:
                self.velocity.x = 0
            self.cur_state = self.states[0]  # standing

    # def jump(self, dt):
    #     """
    #     Basic Jump method for entities.
    #     :param dt: Delta Time
    #     :return: Jump acceleration
    #     """
    #     self.cur_state = [1]

    def update(self, keys, dt):
        """Base update method. Will be filled
            out later."""
        # Gravity and Player Movement

        # PLAYER JUMPING
        # TODO Update code to apply this if statement to check for all tiles rather than the bottom of the screen.
        if self.pos[1] < SCREEN_RES[1] - 40:   # If pos is larger than 40 px off the floor, set state to falling
            self.cur_state = self.states[3]

        if self.cur_state == self.states[0]:   # If current state is standing, do not apply gravity
            self.accel = vec(0.5, 0)

        if self.cur_state == self.states[1]:   # If current state is jumping, add the jump vector
            self.accel = self.jump_vector

        if self.cur_state == self.states[3]:   # If current state is falling, apply gravity
            self.accel = vec(0.5, PLAYER_GRAV)

        self.velocity += self.accel
        self.pos += self.velocity
        self.rect.center = self.pos
        self.move(keys, dt)

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
