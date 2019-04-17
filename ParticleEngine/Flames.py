import pygame, random, math


# dir = math.pi*0.5*math.atan2(dy,dx)
#
#

class Flame(pygame.sprite.Sprite):

    def __init__(self,image,size,pos=(0,0)):
        """Initializes Particle"""
        super().__init__()
        self.size = size
        self.fullImage = image
        self.fullRect = self.fullImage.get_rect()
        self.image = pygame.transform.scale(self.fullImage,(self.size,self.size))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.fullLifeSpan = random.randint(20,41)
        self.originalSize = size
        self.heading = None
        self.originalHeading = None
        self.setHeading(random.uniform(0, 2 * math.pi))
        self.cycleStep = math.pi/14
        self.currentColorIndex = self.fullRect.w-1
        self.colorDelta = int((self.fullRect.w-1)*(1/self.fullLifeSpan)*(3/8))
        self.color = self.fullImage.get_at((self.currentColorIndex,0))
        self.lifespan = 0
        self.dTime = 0
        self.delay = 0
        self.speed = 50

    def setHeading(self,heading):
        """Gives random heading to particle between 0 and 2pi"""
        self.heading = heading
        if self.heading > 1.5*math.pi:
            self.heading -= 2*math.pi
        if self.originalHeading == None:
            self.originalHeading = self.heading

    def move(self,dt):
        """Moves particle in sinusoidal path upward"""
        x,y = self.rect.center

        if self.heading <= 1.5*math.pi and self.heading > math.pi/2:
            self.heading -= self.cycleStep
        elif self.heading < math.pi/2:
            self.heading += self.cycleStep

        x += int(((3 * math.cos(self.heading)) + random.randint(-1,1)))
        if self.heading <= math.pi and self.heading >= 0:
            y -= int(4 * math.sin(self.heading) * dt * self.speed)

        self.rect.center = (x,y)

    def setDelay(self,delay):
        """Sets step delay of particle"""
        self.delay = delay

    def changeSize(self,size):
        """Sets radius of particle effect"""
        self.size = size
        self.originalSize = size

    def update(self,dt):
        """updates particle color and location"""
        self.dTime += dt
        if not self.dTime > self.delay:
            self.dTime += dt
            return

        self.move(dt)

        if self.currentColorIndex > self.fullRect.w*(7/8):
            self.colorDelta = int(self.fullRect.w * (1/8) * (3/40))*2
        elif self.currentColorIndex <= self.fullRect.w*(1/3):
            self.colorDelta = int(self.fullRect.w * (1 / 4) / (40 * (2 / 3)))*2
        else:
            self.currentColorIndex = int(self.fullRect.w/3)

        self.currentColorIndex -= self.colorDelta
        if self.currentColorIndex < 0:
            self.currentColorIndex = 0

        self.color = self.fullImage.get_at((self.currentColorIndex, 0))

        self.image = pygame.transform.scale(self.fullImage,(self.size,self.size))
        self.image.set_alpha(0)
        rect = self.image.get_rect()
        rect.center = self.rect.center
        self.rect = rect
        self.size -= int(self.size / self.lifespan)
        self.lifespan -= 1

    def reset(self,pos):
        """Re-initializes all particle variables"""
        self.rect.center = pos
        self.lifespan = self.fullLifeSpan
        self.size = self.originalSize
        self.currentColorIndex = self.fullRect.w-1
        self.color = self.fullImage.get_at((self.currentColorIndex,0))
        self.setHeading(random.uniform(0, 2 * math.pi))
        self.dTime = 0

    def draw(self,screen, cameraPos):
        """Draws particle on surface"""
        self.image.fill(self.image.get_alpha())
        pygame.draw.circle(self.image,self.color,(int(self.size/2),int(self.size/2)),int(self.size/2))
        screen.blit(self.image,self.rect)

if __name__ == "__main__":
    print("Execute main.py")