from Actor import *


class Enemy(Actor):
    """Basic enemy class that creates the properties/methods shared across all enemies."""

    def __init__(self, spawn_point, img):
        super().__init__(spawn_point)
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

    def draw(self, window):
        window.blit(self.img, self.rect)
