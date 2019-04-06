from Actors.Enemies import Enemy
import pygame

class Boss(Enemy):

    def __init__(self, spawn_point, img, xp_val=100):
        """

        :param spawn_point: x,y position in world to place boss
        :param img: filename of boss sprite
        :param xp_val: xp value of boss to award players upon defeat
        """
        super().__init__(spawn_point, img)
        self.enemyHeight = 94
        for i in self.frames:
            rect = self.frames[i].get_rect()
            width = int(rect.w * (self.enemyHeight / rect.h))
            height = self.enemyHeight
            self.frames[i] = pygame.transform.scale(self.frames[i], (width, height))
            self.frames[i] = self.frames[i].convert_alpha()
        for i in range(len(self.rframes)):
            rect = self.rframes[i].get_rect()
            width = int(rect.w * (self.enemyHeight / rect.h))
            height = self.enemyHeight
            self.rframes[i] = pygame.transform.scale(self.rframes[i], (width, height))
            self.rframes[i] = self.rframes[i].convert_alpha()

        self.rect = self.frames["right"].get_rect()

    def update(self, *args):
        """

        :param args: mouseButtons, keys, dt, projectiles
        :return: void
        """
        super().update(*args)

    def draw(self,window,cameraPos):
        """
        :param window: window to blit image to
        :param cameraPos: offset of world position to place sprite on screen
        :return:
        """
        super().draw(window,cameraPos)

