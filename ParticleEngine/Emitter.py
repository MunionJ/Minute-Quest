import pygame, random, math
from ParticleEngine.Flames import Flame

class Emitter():
    def __init__(self):
        """Initialize Emitter Variables"""
        self.flameSource = "./images/Particle Effects/hp_gradient.png"
        self.fireWorkGradient = pygame.image.load(self.flameSource).convert_alpha()
        self.size = 12
        self.sizeRange = (0,30)
        self.flameParticles = pygame.sprite.Group()
        self.currentButton = None
        self.activeParticles = 0
        self.shouldEmit = False
        self.currentPosition = None
        self.baseColor = pygame.color.THECOLORS['blue']
        self.type = "EMITTER"
        self.bgSurf = pygame.Surface((60,100))
        self.rect = self.bgSurf.get_rect()
        self.alpha = pygame.color.THECOLORS['black']
        self.bgSurf.set_colorkey(self.alpha)
        for i in range(250):
            particle = Flame(self.fireWorkGradient, self.size)
            particle.setDelay(random.uniform(0, 0.15))
            particle.lifespan = random.uniform(0,particle.fullLifeSpan)
            self.flameParticles.add(particle)

    def turnOnParticles(self):
        """Toggle Particle Effects on"""
        self.shouldEmit = True

    def turnOffParticles(self):
        """Toggle Particle Effects on"""
        self.shouldEmit = False

    def setPosition(self,player):
        self.rect.midbottom = player.rect.midbottom

    def moveParticles(self):
        """Moves base of particle emitter to mouse location and recycles dead particles"""
        for particle in self.flameParticles.sprites():
            if particle.lifespan <= 0:
                particle.setDelay(random.uniform(0, 0.15))
                particle.reset((self.rect.w//2,self.rect.h))

    def update(self,*args):
        """Updates all particles and counts active particles"""
        mouseButtons, keys, dt, projectiles = args
        count = 0
        for particle in self.flameParticles.sprites():
            if particle.lifespan > 0:
                particle.update(dt)
                count += 1
        self.activeParticles = count

        if self.shouldEmit:
            self.moveParticles()

    def increaseSize(self):
        """Increases particle size"""
        min,max = self.sizeRange
        if self.size + 1 < max:
            self.size += 1
            for particle in self.flameParticles.sprites():
                particle.changeSize(self.size)

    def decreaseSize(self):
        """Decreases particle Size"""
        min,max = self.sizeRange
        if self.size - 1 > min:
            self.size -= 1
            for particle in self.flameParticles.sprites():
                particle.changeSize(self.size)

    def toggleDebug(self):
        pass

    def draw(self,screen, cameraPos):
        """Draws particles on surface"""
        self.bgSurf.fill(self.alpha)
        for particle in self.flameParticles.sprites():
            if particle.lifespan > 0:
                particle.draw(self.bgSurf, cameraPos)
        pos = (int(self.rect.left-cameraPos[0]),int(self.rect.top - cameraPos[1]))
        screen.blit(self.bgSurf, pos)

if __name__ == "__main__":
    print("Execute main.py")