import pygame

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
        self.prevPos = self.position
        self.velocity = vec(0, 0)
        self.accel = vec(0.5, -0.5)
        self.max_speed = 10
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.debug = False

    def move(self, keys, dt):
        """Base movement method."""

        movedHorizontal = False
        if keys[pygame.K_s]:
            # Implement ability to crouch?
            pass
        if keys[pygame.K_d]:
            self.velocity.x += self.accel.x * dt
            movedHorizontal = True
        elif keys[pygame.K_a]:
            self.velocity -= self.accel.x * dt
            movedHorizontal = True

        # if the entity is not currently moving, decrease their velocity until it reaches 0
        if movedHorizontal:
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

    def update(self, keys, dt):
        """Base update method. Will be filled
            out later."""
        self.move(keys, dt)

    def draw(self):
        """Base draw method. Will be filled
            out later."""
        pass
