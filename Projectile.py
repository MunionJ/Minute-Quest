import pygame
from config import *
import math
vec = pygame.math.Vector2

class Projectile(pygame.sprite.Sprite):

    def __init__(self,fileName, width, height, pos, targetPos, damage = 5, speed=150, targetGameObject = None):
        """
        :param width: width of projectile
        :param height: height of projectile
        :param fileName: string of image filename
        :param pos: start pos of projectile
        :param target: target
        :param speed: speed of projectile
        :param isHoming: determines with the projectile follows target or not
        heading: angle between player and target in degrees
        """

        super().__init__()
        if fileName is not None:
            self.image = pygame.image.load(fileName).convert_alpha() #TODO: change this to image file
        else:
            self.image = pygame.Surface((width,height))
            self.image.set_colorkey(pygame.color.THECOLORS['black'])
            pygame.draw.rect(self.image, pygame.color.THECOLORS['red'], (0, 0, width, height))
        self.image = pygame.transform.scale(self.image, (width,height) )
        self.rect = self.image.get_rect()
        r = min(width,height)

        self.pos = vec(pos[0],pos[1])
        self.velocity = vec(0,0)
        self.accel = vec(0,0)
        self.target = targetPos
        self.speed = speed
        self.targetObject = targetGameObject
        self.heading = None
        self.setHeading(targetPos)
        self.damage = damage
        self.type = "PROJECTILE"
        self.rect.center = (int(self.pos[0]),int(self.pos[1]))


    def update(self, *args):
        """
        :param args: list of mousebuttons,keys currently pressed ,deltatime
        :return:
        """
        dt = args[2]
        if self.targetObject:
            self.setHeading(self.targetObject.rect.center)
        self.move(dt)

    def move(self,dt):
        """

        :param dt: deltaTime
        :return: void
        """

        self.velocity += self.accel * dt
        self.velocity.scale_to_length(MAX_VELOCITY)
        self.pos += self.velocity * dt
        self.rect.center = (int(self.pos.x),int(self.pos.y))


    def setHeading(self,pos):
        """
        :param pos: target position
        :return: void
        """
        endX, endY = pos
        startX, startY = self.pos

        dx = endX - startX
        dy = endY - startY
        heading = math.atan2(-dy,dx)
        heading %= 2*math.pi
        self.accel.x = self.speed*math.cos(heading)
        self.accel.y = -self.speed*math.sin(heading)
        self.heading = heading

    def rotateIMG(self):
        """Rotate image surface to face heading"""

    def draw(self,screen,cameraPos):
        """

        :param screen: window to blit to
        :param cameraPos: offset of camera from worldview
        :return: void
        """
        screen.blit(self.image, (int(self.rect.center[0] - cameraPos[0]), int(self.rect.center[1]-cameraPos[1])))


if __name__ == "__main__":
    import os
    from GameEngine.EventManager import *
    from Scene.Tile import *

    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    bg_color = pygame.color.THECOLORS['black']
    window = pygame.display.set_mode(SCREEN_RES)
    pygame.display.set_caption("PROJECTILE TEST HARNESS")
    manager = EventManager()

    tiles = pygame.sprite.Group()

    bottomY = SCREEN_RES[1] - 32
    topY = 0
    for i in range(int(SCREEN_RES[0] / 32)):
        x = i * 32
        tileSurf = pygame.Surface((32, 32))
        tileSurf.fill(pygame.color.THECOLORS['green'])
        pygame.draw.rect(tileSurf, pygame.color.THECOLORS['black'], pygame.Rect(0, 0, 32, 32), 2)
        topRect = pygame.Rect(x, topY, 32, 32)
        bottomRect = pygame.Rect(x, bottomY, 32, 32)
        tiles.add(Tile(tileSurf, topRect))
        tiles.add(Tile(tileSurf, bottomRect))

        if i == 0 or i == int(SCREEN_RES[0] / 32) - 1:
            for j in range(1, int(SCREEN_RES[0] / 32) - 2):
                tiles.add(Tile(tileSurf, pygame.Rect(x, j * 32, 32, 32)))

    screen_rect = window.get_rect()
    clock = pygame.time.Clock()
    running = True
    projectiles = []

    while running:
        dt = clock.tick(60) / 1000

        # Get Player Input and Apply Physics
        running = manager.process_input(dt,True,projectiles)

        # END COLLISION HANDLING

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    p = Projectile("test",20,10,(SCREEN_RES[0]>>1,SCREEN_RES[1]>>1),pygame.mouse.get_pos())
                    projectiles.append(p)

        for p in projectiles:
            if not screen_rect.colliderect(p.rect):
                projectiles.remove(p)

        window.fill(bg_color)
        pygame.draw.circle(window, pygame.color.THECOLORS['blue'], (SCREEN_RES[0]>>1, SCREEN_RES[1]>>1), 15)

        for p in projectiles:
            p.draw(window, (0,0))
        for obj in manager.game_objects["game_objects"]:
            obj.draw(window, (0,0))

        for tile in tiles.sprites():
            tile.draw(window, (0,0))

        pygame.display.flip()