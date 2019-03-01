import pygame
import random
from Scene.DungeonRoom import *


class Dungeon:
    def __init__(self, num_rooms):
        self.rooms = []
        tempChoices = ROOMS.copy()
        for i in range(num_rooms):

            self.removeEmptyChoices(tempChoices)

            roomType = random.choice(list(tempChoices.keys()))

            roomName = random.choice(ROOMS[roomType])
            tempChoices[roomType].remove(roomName)

            dungeonName = "./maps/{0}/{1}".format(roomType,roomName)

            sprite_sheet = self.assignSpriteSheet(roomName)
            if sprite_sheet == None:
                raise TypeError("Map Name Not Found in Config " + roomName)
            room = DungeonRoom(dungeonName, sprite_sheet)
            self.rooms.append(room)

        self.playerSpawn = self.rooms[0].playerSpawn

        x_offset = self.rooms[0].totalMapWidth

        smallest_y = self.rooms[0].totalMapHeight
        largest_y = self.rooms[0].totalMapHeight
        for i in range(1, num_rooms):
            prevRoom = self.rooms[i-1]
            currentRoom = self.rooms[i]

            rect1 = prevRoom.exitPoint.copy()
            rect2 = currentRoom.playerSpawn.copy()
            prevY = rect2.bottom
            rect2.bottom = rect1.bottom
            y_offset = prevY - rect2.bottom

            currentRoom.bgImageRect.x += x_offset
            currentRoom.bgImageRect.y -= y_offset

            for wall in currentRoom.walls.sprites():
                wall.rect.x += x_offset
                wall.rect.y -= y_offset

            for point in currentRoom.enemySpawnPoints:
                x,y = point.topleft
                x += x_offset
                y += y_offset
                point.topleft = (x, y)

            x, y = currentRoom.exitPoint.topleft
            x += x_offset
            y -= y_offset
            currentRoom.exitPoint.topleft = (x, y)

            currentRoom.boundary.x += x_offset
            currentRoom.boundary.y += y_offset


            x_offset += currentRoom.totalMapWidth
            smallest_y = min(currentRoom.bgImageRect.top,prevRoom.bgImageRect.top)
            largest_y = max(currentRoom.bgImageRect.bottom,prevRoom.bgImageRect.bottom)

        self.totalDungeonWidth = x_offset
        self.totalDungeonHeight = largest_y - smallest_y
        self.boundary = pygame.Rect(0, smallest_y, self.totalDungeonWidth, self.totalDungeonHeight)

        self.dungeonExit = self.rooms[len(self.rooms)-1].exitPoint

    def draw(self,screen):
        for room in self.rooms:
            room.draw(screen)

    def removeEmptyChoices(self, choices):
        badChoices = []
        for key in choices.keys():
            if len(choices[key]) == 0:
                badChoices.append(key)

        r = dict(choices)
        for bc in badChoices:
            del r[bc]

        choices = r

    def assignSpriteSheet(self, roomName):
        for name in WALLS_ONE:
            if name in roomName:
                return "./images/walls1.png"

        for name in UTUMNO:
            if name in roomName:
                return "./images/ProjectUtumno_full.png"

        return None


if __name__ == "__main__":
    import os
    from EventManager import *
    from Scene.Camera import Camera

    running = True
    clock = pygame.time.Clock()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Menu Test")
    screen = pygame.display.set_mode(SCREEN_RES)
    eventManager = EventManager()
    dungeon = Dungeon(4)
    camera = Camera(dungeon)

    camera.reticle.setPos( (SCREEN_RES[0]//2,SCREEN_RES[1]//2) )
    eventManager.addGameObject(camera.reticle)
    for room in dungeon.rooms:
        for wall in room.walls.sprites():
            eventManager.addGameObject(wall)

    while running:
        dt = clock.tick(60) / 1000
        running = eventManager.process_input(dt)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        camera.setCameraPosition(camera.reticle.rect.center)

        screen.fill(pygame.color.THECOLORS['black'])
        camera.draw(screen)
        pygame.display.update()

