import pygame

vec = pygame.math.Vector2


class Actor:
    """This is the base class from which Player,
        Enemy, etc. will inherit from."""
    def __init__(self, start_pos, img):
        # CONSTRUCTOR PARAMETERS #
        # start_pos: a tuple containing a coordinate pair (x, y)
        # img: a .PNG file (a sprite sheet, ideally)

        self.position = vec(start_pos[0], start_pos[1])
        self.velocity = vec(0, 0)
        self.acceleration = vec(0.5, -0.5)
        self.image = pygame.image.load(img)

    def move(self):
        """Base movement method. Will be filled
            out later."""
        pass

    def update(self):
        """Base update method. Will be filled
            out later."""
        pass

    def draw(self):
        """Base draw method. Will be filled
            out later."""
        pass
