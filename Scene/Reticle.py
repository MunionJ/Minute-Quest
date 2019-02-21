import pygame


class Reticle(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((32,32))
        self.image.fill(pygame.color.THECOLORS['black'])
        self.image.set_colorkey(pygame.color.THECOLORS['black'])
        self.rect = self.image.get_rect()
        pygame.draw.line(self.image,pygame.color.THECOLORS['red'],(0,self.rect.h//2),(self.rect.w,self.rect.h//2),3)
        pygame.draw.line(self.image,pygame.color.THECOLORS['red'],(self.rect.w//2,0),(self.rect.w//2,self.rect.h),3)
        self.speed = 500
        self.pos = [self.rect.center[0],self.rect.center[1]]

    def setPos(self,pos):
        self.pos[0],self.pos[1] = pos
        self.rect.center = (int(pos[0]),int(pos[1]))

    def update(self,keys,dt):

        dx = 0
        dy = 0
        if keys[pygame.K_a]:
            dx = -(self.speed*dt)
        if keys[pygame.K_w]:
            dy = -(self.speed*dt)
        if keys[pygame.K_d]:
            dx = (self.speed*dt)
        if keys[pygame.K_s]:
            dy = (self.speed*dt)

        self.pos[0] += dx
        self.pos[1] += dy
        self.rect.center = (int(self.pos[0]),int(self.pos[1]))