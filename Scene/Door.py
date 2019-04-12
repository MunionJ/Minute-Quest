import pygame


class Door(pygame.sprite.Sprite):
    """ This class handles information
        about each individual Tile in the map."""

    def __init__(self, imageSurf, rect):
        super().__init__()
        self.image = imageSurf
        self.rect = rect
        self.debug = False
        self.type = "DOOR"

    def toggleDebug(self):
        self.debug = not self.debug

    def draw(self,screen, cameraPos):
        screen.blit(
            self.image,
            (int(self.rect.x - cameraPos[0]), int(self.rect.y - cameraPos[1]))
        )
        if self.debug:
            debug = pygame.Rect(int(self.rect.x - cameraPos[0]), int(self.rect.y - cameraPos[1]),self.rect.w,self.rect.h)
            pygame.draw.rect(screen, pygame.color.THECOLORS['red'], debug,1)



