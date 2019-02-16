import pygame

class Button(pygame.sprite.Sprite):

    def __init__(self, fontSurf, x=0,y=0,w=20,h=20,bgColor=pygame.color.THECOLORS['blue'],selectionColor=pygame.color.THECOLORS['yellow']):
        super().__init__()
        self.fontSurf = fontSurf
        self.fontRect = self.fontSurf.get_rect()
        self.rect = pygame.Rect(x, y, max(w, self.fontRect.w), max(h, self.fontRect.h))
        self.surf = pygame.Surface((self.rect.w,self.rect.h))
        self.bgColor = bgColor
        self.selectionColor = selectionColor
        self.surf.fill(self.bgColor)
        self.surf.blit(self.fontSurf,self.fontRect)
        self.isSelected = False
        self.selectionRect = self.rect.copy()
        self.selectionRect.w = self.selectionRect.w + 4
        self.selectionRect.h = self.selectionRect.h + 4

    def updateLocation(self,x,y):
        """Centers button on x,y coordinates passed"""
        self.rect.center = (int(x),int(y))
        self.selectionRect.center = self.rect.center

    def select(self):
        self.isSelected = True

    def deselect(self):
        self.isSelected = False

    def toggleDebug(self):
        pass

    def draw(self,window):
        self.surf.fill(self.bgColor)
        self.surf.blit(self.fontSurf,(self.rect.w//2 - self.fontRect.w//2, self.rect.h//2 - self.fontRect.h//2))
        window.blit(self.surf,self.rect)
        if self.isSelected:
            pygame.draw.rect(window,self.selectionColor,self.selectionRect,6)