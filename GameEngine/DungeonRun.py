from Scene.Camera import *
from GameEngine.GameHUD import *
from Actors.Party import *
from Actors.Enemies import *


class DungeonRun:

    def __init__(self, event_mgr, game_window, party=None):
        self.window = game_window
        self.manager = event_mgr
        self.running = False
        self.dungeon = Dungeon(4)
        if party is None:
            self.party_list = Party(self.dungeon.playerSpawn)
        else:
            self.party_list = party
        self.player = self.party_list.active_member
        self.player.rect.bottom = self.dungeon.playerSpawn.bottom
        self.camera = Camera(self.dungeon)
        self.camera.setCameraPosition(self.player.rect.center)
        self.manager.addGameObject(self.player)
        self.manager.addParty(self.party_list)
        self.HUD = GameHUD(self.window)
        self.manager.addGameObject(self.HUD)
        self.clock = pygame.time.Clock()
        self.bg_color = pygame.color.THECOLORS["black"]
        self.prev_room = self.dungeon.rooms[0]
        for room in self.dungeon.rooms:
            for wall in room.walls.sprites():
                self.manager.addGameObject(wall)
        self.enemiesByRoom = []
        for room in self.dungeon.rooms:
            enemy_list = []
            for enemyspawnpoint in room.enemySpawnPoints:
                enemy = Enemy(enemyspawnpoint.midbottom,
                              "images/Characters/enemy1",
                              100,
                              2)  # TODO incorporate Party.calc_avg_level() method for Enemy level parameter
                enemy_list.append(enemy)
                self.manager.addGameObject(enemy)
            room.enemies = enemy_list
            self.enemiesByRoom.append(enemy_list)
        self.gameOverScreen = pygame.Surface(SCREEN_RES)
        self.font = pygame.font.Font('./fonts/LuckiestGuy-Regular.ttf', 100)
        self.gameOverCondition = None
        self.fontSurface = None
        self.font_color = pygame.color.THECOLORS['red']
        self.postTime = 3
        self.projectiles = []
        self.playerBoundary = self.dungeon.rooms[0].bgImageRect

    def start_game(self):
        self.running = True

    def launch_game(self):
        while self.running:
            dt = self.clock.tick(60) / 1000
            if self.gameOverCondition and self.postTime > 0:
                self.postTime -= dt
                fontSurface = self.font.render(self.gameOverCondition, False, self.font_color)
                fontrect = fontSurface.get_rect()
                fontrect.center = (SCREEN_RES[0] >> 1, SCREEN_RES[1] >> 1)
                self.window.fill(pygame.color.THECOLORS['black'])
                self.window.blit(fontSurface, fontrect)
                self.manager.poll_input(dt)
            else:
                if self.postTime <= 0:
                    if self.player.rect.x > self.dungeon.rooms[len(self.dungeon.rooms) - 1].bgImageRect.x:
                        self.gameWin()
                    else:
                        self.gameOver()
                    break

                self.running = self.manager.process_input(dt, (
                    not (self.player.class_name == "WIZARD" and self.player.usingAbility)), self.projectiles)
                self.running = self.manager.poll_input(dt)
                self.player_swap_cd(dt)
                cur_pos = self.player.rect
                self.manager.removeGameObject(self.player)
                self.player = self.party_list.active_member
                self.manager.addGameObject(self.player)
                self.player.set_pos(cur_pos)

                for i in range(len(self.dungeon.rooms)):
                    room = self.dungeon.rooms[i]
                    if room.bgImageRect.colliderect(self.player.rect):
                        if len(room.enemies) > 0:
                            for enemy in room.enemies:
                                distance = self.player.pos - enemy.pos
                                if distance.length() < ENEMY_VISION_RANGE:
                                    enemy.line_of_sight(self.window, self.camera.pos, self.player, room.walls)
                        if i + 1 < len(self.dungeon.rooms):
                            self.playerBoundary = room.objective.evaluateObjective(self.player, self.playerBoundary,
                                                                                   self.dungeon.rooms[i + 1],
                                                                                   room.enemies)
                            rect = self.player.rect.clamp(self.playerBoundary)
                            self.player.set_pos(rect)
                # events = pygame.event.get()
                # for event in events:
                #     if event.type == pygame.QUIT:
                #         self.running = False

                if self.player.usingAbility:
                    if self.player.class_name == "WIZARD":
                        self.HUD.timer += dt
                    elif self.player.class_name == "PALADIN":
                        self.player.heal_party(self.party_list)

                self.collisionHandling(dt)
                self.addProjectiles()

                # Win Condition
                if not self.player.alive:
                    prevRect = self.player.rect
                    self.manager.removeGameObject(self.player)
                    self.party_list.swapPlayer()
                    self.player = self.party_list.active_member
                    self.player.set_pos(prevRect)
                    self.manager.addGameObject(self.player)

                if self.player.pos.x >= self.dungeon.dungeonExit.left:
                    self.gameWin()

                # Lose Conditions
                if self.outOfBounds(self.player.rect.center) or self.allPlayersDead():
                    self.gameOverCondition = "You Died!"

                if self.HUD.getTime() <= 0:
                    self.gameOverCondition = "Times Up!"

                self.camera.setCameraPosition(self.player.rect.center)
                pygame.draw.rect(self.window, (255, 255, 255), self.player.rect, 2)
                self.window.fill(self.bg_color)
                self.camera.draw(self.window, self.player, self.enemiesByRoom, self.projectiles)
                self.fadeEffect()
                self.HUD.draw(self.window, self.party_list, dt)
            pygame.display.flip()

    def player_swap_cd(self, dt):
        """ 3 second cooldown on switching
            active party member."""
        self.party_list.last_active += dt
        # print(self.party_list.last_active)

    def allPlayersDead(self):
        for player in self.party_list.party_members:
            if player.stats['CUR_HP'] > 0:
                return False
        return True

    def outOfBounds(self, playerPos):
        for room in self.camera.dungeon.rooms:
            bounds = room.bgImageRect
            if bounds.collidepoint(playerPos):
                return False
        return True

    def collisionHandling(self, dt):
        """ Move Player and Check for Collisions"""

        hasCollided = False
        for room in self.dungeon.rooms:
            if self.player.rect.colliderect(room.bgImageRect):
                hasCollided = True
                objective = room.objective.getAnnouncement()
                self.HUD.getRoomObj(objective)
                break

        if not hasCollided:
            self.gameOver()

        currentRoomIndex = None
        roomWidth = self.dungeon.rooms[0].bgImageRect.w
        tiles = pygame.sprite.Group()

        cur_index = 0
        for i in range(len(self.dungeon.rooms)):
            if self.player.rect.colliderect(self.dungeon.rooms[i].bgImageRect):
                cur_index = i
                break
        tiles.add(self.dungeon.rooms[cur_index].walls.sprites())

        self.collisionCheck(tiles, dt)

        for p in self.projectiles:
            if not p.hitbox.colliderect(self.dungeon.rooms[cur_index].bgImageRect):
                if self.manager.hasReferenceToGameObject(p):
                    self.manager.removeGameObject(p)
                    self.projectiles.remove(p)
                    continue

            for tile in tiles:
                if tile.rect.colliderect(p.hitbox):
                    if self.manager.hasReferenceToGameObject(p):
                        self.manager.removeGameObject(p)
                        self.projectiles.remove(p)

    def collisionCheck(self, tiles, dt):

        # keep track of killed enemies to award xp
        flagged_enemies = []
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
                rect.move_ip(0, 1)
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

        for room in self.dungeon.rooms:
            if self.player.rect.colliderect(room.bgImageRect):
                # handle objective display
                if self.prev_room != room:
                    self.prev_room = room
                    self.HUD.reset_objective_timer()

                for enemy in room.enemies:
                    for p in self.projectiles:
                        if p.hitbox.colliderect(enemy.rect):
                            enemy.take_damage(p)
                            if self.manager.hasReferenceToGameObject(p):
                                self.manager.removeGameObject(p)
                                self.projectiles.remove(p)
                                if not enemy.alive:
                                    flagged_enemies.append(enemy)
                                    room.enemies.remove(enemy)

                for enemy in room.enemies:
                    if (not self.manager.hasReferenceToGameObject(enemy)):
                        self.manager.addGameObject(enemy)
                    enemy.moveX(dt)
                    collisions = pygame.sprite.spritecollide(enemy, tiles, False)
                    if collisions:
                        hit = collisions[0]
                        enemy.handleXCollision(hit.rect)

                    enemy.moveY(dt)
                    collisions = pygame.sprite.spritecollide(enemy, tiles, False)

                    vertCollisions = False
                    if collisions:
                        hit = collisions[0]
                        vertCollisions = enemy.handleYCollision(hit.rect)

                    rect = enemy.rect.copy()

                    if not vertCollisions:
                        for i in range(PIXEL_DIFFERENCE):
                            rect.move_ip(0, 1)
                            for wall in tiles.sprites():
                                if rect.colliderect(wall.rect) and enemy.velocity.y >= 0:
                                    enemy.handleYCollision(wall.rect)
                                    vertCollisions = True
                                    break
                            if vertCollisions:
                                break

                    if not vertCollisions:
                        enemy.isInAir()

                    rect = enemy.rect.clamp(room.bgImageRect)
                    enemy.set_pos(rect)

                    enemy.determineState()

                    for enemy in room.enemies:
                        if self.player.rect.colliderect(enemy.rect):
                            self.player.receive_dmg(enemy)

                if self.player.cur_weapon is not None:
                    # print("DungeonRun.py: Line 244: ", self.player.cur_weapon.active)
                    if self.player.cur_weapon.active:
                        for enemy in room.enemies:
                            if self.player.cur_weapon.rect.colliderect(enemy.rect):
                                # print("DungeonRun.py: Line 247: ", self.player.cur_weapon.rect.colliderect(enemy.rect))
                                enemy.take_damage(self.player)
                                if not enemy.alive:
                                    flagged_enemies.append(enemy)
                                    room.enemies.remove(enemy)


            else:
                for enemy in room.enemies:
                    if self.manager.hasReferenceToGameObject(enemy):
                        self.manager.removeGameObject(enemy)
        self.party_list.award_xp(flagged_enemies)
        flagged_enemies.clear()

    def addProjectiles(self):
        for p in self.projectiles:
            if not self.manager.hasReferenceToGameObject(p):
                self.manager.addGameObject(p)

    def gameWin(self):
        "Award Experience and level up"
        self.running = False

    def gameOver(self):
        "The Player's Experience gets reset"
        self.running = False

    def fadeEffect(self):
        finalRoomX = self.dungeon.rooms[len(self.dungeon.rooms) - 1].bgImageRect.x
        if self.player.rect.x > finalRoomX:
            # Fade to White
            fullP = self.dungeon.dungeonExit.x - finalRoomX
            curP = self.player.rect.x - finalRoomX
            alphaLevel = int(255 * (curP / fullP))
            overlay = pygame.Surface(SCREEN_RES)
            overlay.fill((255, 255, 255))
            overlay.set_alpha(alphaLevel)
            self.window.blit(overlay, (0, 0))
