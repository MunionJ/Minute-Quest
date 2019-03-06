import pygame
from Scene.Tile import Tile
from Scene.Dungeon import *
from Scene.Reticle import *
import math

class Camera():

    def __init__(self, dungeon):
        self.dungeon = dungeon
        self.pos = (0,0)
        self.prevPos = (0,0)
        self.boundary = dungeon.boundary
        self.view = pygame.Surface(SCREEN_RES)
        self.rect = self.view.get_rect()

        self.debug = False
        self.reticle = Reticle()
        self.bg_color = pygame.color.THECOLORS['black']

    def setCameraPosition(self,playerPos):
        """Updates camera position based on location of player"""
        topLeftX = playerPos[0] - (SCREEN_RES[0] / 2)
        topLeftY = playerPos[1] - (SCREEN_RES[1] / 2)

        roomIndex = self.getRoomIndex(playerPos)
        #currentRoom = self.dungeon.rooms[roomIndex].bgImageRect

        # if topLeftX < 0:
        #     topLeftX = 0
        # elif topLeftX + SCREEN_RES[0] >= self.dungeon.playerBounds.w:
        #     topLeftX = self.dungeon.playerBounds.w - SCREEN_RES[0]
        #
        # if topLeftY <= self.dungeon.playerBounds.y:
        #     topLeftY = self.dungeon.playerBounds.y
        # elif topLeftY + SCREEN_RES[1] >= self.dungeon.playerBounds.y + self.dungeon.playerBounds.h:
        #     topLeftY = self.dungeon.playerBounds.y + self.dungeon.playerBounds.h - SCREEN_RES[1]

        self.pos = (topLeftX, topLeftY)

        #possibly only call this when the player has moved enough to scroll
        self.updateMapView()

    def getRoomIndex(self,playerPos):
        for i in range(len(self.dungeon.rooms)):
            room = self.dungeon.rooms[i].bgImageRect
            if playerPos[0] in range(room.x, room.x + room.w):
                return i
        return None

    def updateMapView(self):
        """Grabs tiles out of map and blits them to the camera viewing surface"""
        self.view.fill(self.bg_color)
        for map in self.dungeon.rooms:
            self.view.blit(
                map.bgImage,
                (int(map.bgImageRect.x - self.pos[0]),int(map.bgImageRect.y - self.pos[1]))
            )

            bg_rect = pygame.Rect(
                int(map.bgImageRect.x - self.pos[0]),
                int(map.bgImageRect.y - self.pos[1]),
                map.bgImageRect.w,
                map.bgImageRect.h
            )
            pygame.draw.rect(
                self.view,
                pygame.color.THECOLORS['red'],
                bg_rect,
                5
            )

    def toggleDebug(self):
        """ Toggles the debug flag, which signals
            whether to draw debug information to
            the game screen."""
        self.debug = not self.debug

    def draw(self, screen, player, enemy_list):
        for map in self.dungeon.rooms:
            if self.dungeon.playerBounds.colliderect(map.bgImageRect):
                screen.blit(
                    map.bgImage,
                    (int(map.bgImageRect.x - self.pos[0]),int(map.bgImageRect.y - self.pos[1]))
                )

                for wall in map.walls:
                    screen.blit(
                        wall.image,
                        (int(wall.rect.x - self.pos[0]),int(wall.rect.y - self.pos[1]))
                    )

                bg_rect = pygame.Rect(
                    int(map.bgImageRect.x - self.pos[0]),
                    int(map.bgImageRect.y - self.pos[1]),
                    map.bgImageRect.w,
                    map.bgImageRect.h
                )
            else:
                break
        for enemy in enemy_list:
            screen.blit(enemy.img,
                        (int(enemy.rect.x - self.pos[0]), int(enemy.rect.y - self.pos[1])))
        screen.blit(
            player.image,
            (player.rect.x - self.pos[0], player.rect.y - self.pos[1])
                    )




    def update(self,*args):
        pass


if __name__ == "__main__":
    import os
    from EventManager import *

    running = True
    clock = pygame.time.Clock()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Menu Test")
    screen = pygame.display.set_mode(SCREEN_RES)
    eventManager = EventManager()
    camera = Camera(map)

    camera.reticle.setPos( camera.dungeon.playerSpawn.center )
    eventManager.addGameObject(camera.reticle)
    for room in camera.dungeon.rooms:
        for wall in room.walls.sprites():
            eventManager.addGameObject(wall)

    while running:
        dt = clock.tick(60)/1000
        running = eventManager.process_input(dt)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        camera.setCameraPosition(camera.reticle.rect.center)

        screen.fill(pygame.color.THECOLORS['black'])
        camera.draw(screen)
        pygame.display.update()