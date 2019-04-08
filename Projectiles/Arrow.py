from Projectiles.Projectile import Projectile
import math
import pygame

class Arrow(Projectile):

    def __init__(self, fileName, width, height, pos, targetPos, damage=1, speed=150, targetGameObject=None):
        super().__init__(fileName, width, height, pos, targetPos, damage, speed, targetGameObject)
        self.hitbox = None
        self.determine_hitbox()
        self.dif_x_pos = self.hitbox.center[0] - self.rect.center[0]
        self.dif_y_pos = self.hitbox.center[1] - self.rect.center[1]

    def determine_hitbox(self):
        hitbox_width = self.rect.w // 3
        hitbox_height = self.rect.h // 3
        hitbox_x = math.cos(self.heading) * (.5 * self.rect.w) + self.rect.center[0]
        hitbox_y = -math.sin(self.heading) * (.5 * self.rect.h) + self.rect.center[1]
        self.hitbox = pygame.Rect(0,0, hitbox_width, hitbox_height)
        self.hitbox.center = (hitbox_x,hitbox_y)

    def update(self, *args):
        super().update(*args)
        self.hitbox.center = (self.dif_x_pos + self.rect.center[0], self.dif_y_pos+self.rect.center[1])


    def draw(self, screen, cameraPos):
        super().draw(screen, cameraPos)
        pygame.draw.rect(screen, pygame.color.THECOLORS['red1'], (self.hitbox.x - cameraPos[0], self.hitbox.y - cameraPos[1]
                                                                  , self.hitbox.w, self.hitbox.h), 1)
