from Player import *
from Scene.Camera import *

class Game:

    def __init__(self, event_mgr, game_window):
        self.window = game_window
        self.manager = event_mgr
        self.running = False
        self.dungeon = Dungeon(4)
        self.player = Player(self.dungeon.playerSpawn, "images/character1")
        self.player.rect.bottom = self.dungeon.playerSpawn.bottom
        self.camera = Camera(self.dungeon)
        self.camera.setCameraPosition(self.player.rect.center)
        self.manager.addGameObject(self.player)
        self.clock = pygame.time.Clock()
        self.bg_color = pygame.color.THECOLORS["black"]
        for room in self.dungeon.rooms:
            for wall in room.walls.sprites():
                self.manager.addGameObject(wall)

    def start_game(self):
        self.running = True

    def launch_game(self):
        while self.running:
            dt = self.clock.tick(60) / 1000

            self.running = self.manager.process_input(dt)

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            self.collisionHandling(dt)

            #Win Condition
            if self.player.pos.x >= self.dungeon.dungeonExit.left:
                self.gameWin()


            self.camera.setCameraPosition(self.player.rect.center)
            # print(self.player.rect.center, self.player.pos)
            pygame.draw.rect(self.window, (255, 255, 255), self.player.rect, 2)



            self.window.fill(self.bg_color)
            self.camera.draw(self.window, self.player)
            pygame.display.flip()


    def collisionHandling(self,dt):
        """ Move Player and Check for Collisions"""

        hasCollided = False
        for room in self.dungeon.rooms:
            if self.player.rect.colliderect(room.bgImageRect):
                hasCollided = True
                break

        if not hasCollided:
            self.gameOver()

        currentRoomIndex = None
        roomWidth = self.dungeon.rooms[0].bgImageRect.w
        tiles = pygame.sprite.Group()
        for i in range(len(self.dungeon.rooms)):
            if self.player.rect.colliderect(self.dungeon.rooms[i].bgImageRect):
                tiles.add(self.dungeon.rooms[i].walls.sprites())

        self.collisionCheck(tiles,dt)

    def collisionCheck(self,tiles,dt):

        self.player.moveX(dt)
        collisions = pygame.sprite.spritecollide(self.player, tiles, False)
        if collisions:
            hit = collisions[0]
            self.player.handleXCollision(hit.rect)

        self.player.moveY(dt)
        collisions = pygame.sprite.spritecollide(self.player, tiles, False)

        vertCollisions = False
        if collisions:
            hit = collisions[0]
            vertCollisions = self.player.handleYCollision(hit.rect)

        rect = self.player.rect.copy()

        if not vertCollisions:
            for i in range(PIXEL_DIFFERENCE):
                rect.move_ip(0,1)
                for wall in tiles.sprites():
                    if rect.colliderect(wall.rect) and self.player.velocity.y >= 0:
                        self.player.handleYCollision(wall.rect)
                        vertCollisions = True
                        break
                if vertCollisions:
                    break

        if not vertCollisions:
            self.player.isInAir()

        self.player.determineState()

    def gameWin(self):
        "Award Experience and level up"
        self.running = False

    def gameOver(self):
        "The Player's Experience gets reset"
        self.running = False