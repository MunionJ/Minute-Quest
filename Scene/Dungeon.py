import random
from Scene.DungeonRoom import *
import copy
from config import *


class Dungeon:
    def __init__(self, num_rooms):
        """
            Creates dungeon rooms by aligning entrance and exit points
            :param num_rooms: number of rooms with objectives that should be created
        """
        self.rooms = []
        tempChoices = copy.deepcopy(ROOMS)
        self.dirt = pygame.image.load("./images/map_dirt_background.png")
        self.dirt = pygame.transform.scale(self.dirt, SCREEN_RES)

        entrance = DungeonRoom("./maps/entrance.txt","./images/ProjectUtumno_full.png")
        self.rooms.append(entrance)

        for i in range(num_rooms):

            dice = random.randint(0, 100)

            roomType = None

            while roomType == None:

                if dice == 0 and len(tempChoices['LootRooms']) > 0:
                    roomType = "LootRooms"

                elif dice < 41 and len(tempChoices['EnemyRooms']) > 0:
                    roomType = "EnemyRooms"

                elif dice < 82 and len(tempChoices['PlatformRooms']) > 0:
                    roomType = "PlatformRooms"

                elif len(tempChoices['PuzzleRooms']) > 0:
                    roomType = "PuzzleRooms"

            tempChoices = self.removeEmptyChoices(tempChoices)
            roomName = random.choice(tempChoices[roomType])
            tempChoices[roomType].remove(roomName)
            dungeonName = "./maps/{0}/{1}".format(roomType, roomName)
            print(dungeonName)
            sprite_sheet = self.assignSpriteSheet(roomName)
            if sprite_sheet == None:
                raise TypeError("Map Name Not Found in Config " + roomName)
            room = DungeonRoom(dungeonName, sprite_sheet)
            self.rooms.append(room)

        exit = DungeonRoom("./maps/Exit Room.txt", "./images/ProjectUtumno_full.png")
        self.fillExitBG(exit)
        self.rooms.append(exit)

        self.playerSpawn = self.rooms[0].playerSpawn

        x_offset = self.rooms[0].totalMapWidth

        smallest_y = self.rooms[0].totalMapHeight
        largest_y = self.rooms[0].totalMapHeight
        for i in range(1, len(self.rooms)):
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
                point.x += x_offset
                point.y -= y_offset

            for key in currentRoom.possibleKeys:
                key.rect.x += x_offset
                key.rect.y -= y_offset

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
        self.smallest_y = smallest_y

        self.boundary = pygame.Rect(0, smallest_y, self.totalDungeonWidth, self.totalDungeonHeight)
        self.playerBounds = self.boundary
        self.dungeonExit = self.rooms[len(self.rooms)-1].exitPoint




    def fillExitBG(self,exit):
        """
            Draws dirt background to Dungeon exit room
            :param exit: Last room in dungeon
            :return: void
        """
        dirtRect = self.dirt.get_rect()
        cols = exit.bgImageRect.w // dirtRect.w
        startY = exit.exitPoint.bottom
        newBGSurf = pygame.Surface((exit.bgImageRect.w,exit.bgImageRect.h))
        while startY < exit.bgImageRect.bottom:
            x = 0
            while x < exit.bgImageRect.w:
                newBGSurf.blit(self.dirt,(x,startY))
                x+= dirtRect.w
            startY += dirtRect.h

        exit.bgImage = newBGSurf


    def drawBackGround(self,screen,cameraPos):
        """
            Test Method to draws game background
            :param screen: screen to draw to
            :param cameraPos: current camera position
            :return: void
        """
        x_offset = cameraPos[0] % SCREEN_RES[0]
        y_offset = self.dungeonExit.bottom - cameraPos[1]
        print(x_offset, y_offset)

        y = y_offset
        while y < SCREEN_RES[1]+cameraPos[1]:
            screen.blit(self.dirt, (SCREEN_RES[0] - x_offset, y))
            screen.blit(self.dirt, (-x_offset, y))
            y += self.dirt.get_rect().h


    def draw(self,screen, cameraPos):
        """
            Draws the Dungeon
            :param screen: pygame window to draw to
            :param cameraPos: current camera position
            :return: void
        """
        #self.drawBackGround(screen,cameraPos)
        for room in self.rooms:
            room.draw(screen, cameraPos)

    def removeEmptyChoices(self, choices):
        """
            Removes empty choices after random selection
            :param choices: map of rooms to be modified
            :return: map of valid room choices
        """
        badChoices = []
        for key in choices.keys():
            if len(choices[key]) == 0:
                badChoices.append(key)

        r = dict(choices)
        for bc in badChoices:
            del r[bc]

        return r

    def assignSpriteSheet(self, roomName):
        """
            Determines which sprite sheet to pull tiles from
            :param roomName: Name of room
            :return: void
        """
        for name in WALLS_ONE:
            if name in roomName:
                return "./images/walls1.png"

        for name in UTUMNO:
            if name in roomName:
                return "./images/ProjectUtumno_full.png"

        return None


if __name__ == "__main__":
    import os
    from GameEngine.EventManager import *
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

