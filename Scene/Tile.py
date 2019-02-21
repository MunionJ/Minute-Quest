import pygame


class Tile(pygame.sprite.Sprite):
    """ This class handles information
        about each individual Tile in the map."""

    def __init__(self, imageSurf, rect):
        super().__init__()
        self.image = imageSurf
        self.rect = rect
        self.debug = False

    def toggleDebug(self):
        self.debug = not self.debug

    def draw(self,win):
        win.blit(self.image,self.rect)
        if self.debug:
            pygame.draw.rect(win, pygame.color.THECOLORS['red'], self.rect,1)



