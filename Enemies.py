from Actor import *


class Enemy(Actor):
    """Basic enemy class that creates the properties/methods shared across all enemies."""

    def __init__(self, spawn_point, img):
        super().__init__(spawn_point)
        self.img = pygame.image.load(img + "/right1.png")
        self.rect = self.img.get_rect()

    def move(self, keys, dt):
        pass

    def draw(self, window):
        super().draw(window)
        window.blit(self.img, self.rect)
