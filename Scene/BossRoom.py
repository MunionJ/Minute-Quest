from Scene.DungeonRoom import *
from config import *

class BossRoom:
    def __init__(self, SCREEN_RES):
        """
            Creates dungeon rooms by aligning entrance and exit points
            :param num_rooms: number of rooms with objectives that should be created
        """
        self.rooms = []
        self.SCREEN_RES = SCREEN_RES
        entrance = DungeonRoom("./maps/entrance.txt","./images/ProjectUtumno_full.png")
        self.rooms.append(entrance)

        bossRoom = DungeonRoom("./maps/boss rooms/boss room1.txt", "./images/walls1.png")
        self.rooms.append(bossRoom)

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

            x, y = currentRoom.exitPoint.topleft
            x += x_offset
            y -= y_offset
            currentRoom.exitPoint.topleft = (x, y)

            x,y = currentRoom.playerSpawn.topleft
            x = rect1.right
            y -= y_offset
            currentRoom.playerSpawn.topleft = (x,y)

            x_offset += currentRoom.totalMapWidth
            smallest_y = min(currentRoom.bgImageRect.top,prevRoom.bgImageRect.top)
            largest_y = max(currentRoom.bgImageRect.bottom,prevRoom.bgImageRect.bottom)

        self.totalDungeonWidth = x_offset
        self.totalDungeonHeight = largest_y - smallest_y
        self.smallest_y = smallest_y

        self.dungeonExit = self.rooms[len(self.rooms)-1].exitPoint


    def draw(self,screen, cameraPos):
        """
            Draws the Dungeon
            :param screen: pygame window to draw to
            :param cameraPos: current camera position
            :return: void
        """
        for room in self.rooms:
            room.draw(screen, cameraPos)

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

