from Actor import *


class Enemy(Actor):
    """Basic enemy class that creates the properties/methods shared across all enemies."""

    def __init__(self, spawn_point, img):
        super().__init__(spawn_point, img + "/right1.png")
        self.img = pygame.image.load(img + "/right1.png")

    def update(self, dt):
        """
        Updates enemy position and applies physics.
        :param dt: DeltaTime
        :return: None
        """
        self.apply_physics()

        self.velocity += self.accel * dt
        self.pos += self.velocity
        self.rect.center = self.pos

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
        window.blit(self.img, self.rect)
