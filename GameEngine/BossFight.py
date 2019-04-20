from Scene.Camera import Camera
from Scene.Objective import *
from GameEngine.GameHUD import GameHUD
from GameEngine.Credits import Credits
from Actors.Party import Party
from Actors.Boss import Boss
from Scene.BossRoom import BossRoom
from config import  PIXEL_DIFFERENCE
from Scene.Loading import Loading
import pygame
import time
from ParticleEngine.Emitter import Emitter


class BossFight:

    def __init__(self, event_mgr, game_window, game_save_info):
        self.window = game_window
        x,y,w,h = self.window.get_rect()
        self.SCREEN_RES = (w,h)
        self.manager = event_mgr
        self.running = False
        self.dungeon = BossRoom(self.SCREEN_RES)
        self.party_list = Party(self.dungeon.playerSpawn)
        if game_save_info != None:
            self.party_list.loadPartyInfoFromSave(game_save_info)
        self.player = self.party_list.active_member
        self.player.rect.bottom = self.dungeon.playerSpawn.bottom
        self.camera = Camera(self.dungeon)
        self.camera.setCameraPosition(self.player.rect.center)
        self.manager.addGameObject(self.player)
        self.manager.addParty(self.party_list)
        self.HUD = GameHUD(self.window)
        self.manager.addGameObject(self.HUD)
        self.clock = pygame.time.Clock()
        self.loading = Loading(self.SCREEN_RES)
        self.bg_color = pygame.color.THECOLORS["black"]
        self.prev_room = self.dungeon.rooms[0]
        for room in self.dungeon.rooms:
            for wall in room.walls.sprites():
                self.manager.addGameObject(wall)
        self.enemiesByRoom = []
        for room in self.dungeon.rooms:
            enemy_list = []
            for enemyspawnpoint in room.enemySpawnPoints:
                enemy = Boss(enemyspawnpoint.midbottom,
                             "./images/Characters/boss2",
                             200,
                             self.party_list.avg_level + 1) # make Boss 1 level higher than party average
                enemy_list.append(enemy)
                self.manager.addGameObject(enemy)
            room.enemies = enemy_list
            self.enemiesByRoom.append(enemy_list)
        self.gameOverScreen = pygame.Surface(self.SCREEN_RES)
        self.font = pygame.font.Font('./fonts/LuckiestGuy-Regular.ttf', 100)
        self.gameOverCondition = None
        self.fontSurface = None
        self.font_color = pygame.color.THECOLORS['red']
        self.postTime = 3
        self.projectiles = []
        self.boss = self.enemiesByRoom[1][0]
        self.particleEmitter = Emitter()
        self.manager.addGameObject(self.particleEmitter)

    def start_game(self):
        self.running = True

    def launch_game(self):
        while self.running:
            dt = self.clock.tick(60) / 1000
            if self.gameOverCondition and self.postTime > 0:
                self.postTime -= dt
                fontSurface = self.font.render(self.gameOverCondition,False,self.font_color)
                fontrect = fontSurface.get_rect()
                fontrect.center = (self.SCREEN_RES[0]>>1,self.SCREEN_RES[1]>>1)
                self.window.fill(pygame.color.THECOLORS['black'])
                self.window.blit(fontSurface,fontrect)
                self.manager.poll_input(dt)
            else:
                if self.postTime <= 0:
                    if self.player.rect.x > self.dungeon.rooms[len(self.dungeon.rooms)-1].bgImageRect.x:
                        self.gameWin()
                    else:
                        self.gameOver()
                    break

                self.running = self.manager.process_input(dt, (not (self.player.class_name=="WIZARD" and self.player.usingAbility)), self.projectiles)
                self.running = self.manager.poll_input(dt)

                #Swaps Another Party Member to the active Player Position
                self.player_swap_cd(dt)
                cur_pos = self.player.rect
                self.manager.removeGameObject(self.player)
                self.player = self.party_list.active_member
                self.manager.addGameObject(self.player)
                self.player.set_pos(cur_pos)

                for i in range(len(self.dungeon.rooms)):
                    room = self.dungeon.rooms[i]
                    if len(room.enemies) > 0:
                        if room.bgImageRect.colliderect(self.player.rect):
                            for wall in room.walls:
                                if not self.manager.hasReferenceToGameObject(wall):
                                    self.manager.addGameObject(wall)

                            for enemy in room.enemies:
                                if not enemy.alive:
                                    if self.manager.hasReferenceToGameObject(enemy):
                                        self.manager.removeGameObject(enemy)
                                        room.enemies.remove(enemy)
                                else:   #do i have line of sight
                                    distance = self.player.pos - enemy.pos
                                    if distance.length() < enemy.vision_range:
                                        enemy.line_of_sight(self.window, self.camera.pos, self.player, room.walls)

                            room.objective.evaluateObjective(self.player, room.enemies, room.selectedKey, room.Puzzlerects)
                            if not room.objective.isComplete():
                                if room.exitDoor == None:
                                    room.lockDoors(self.player)
                            else:
                                if self.manager.hasReferenceToGameObject(room.exitDoor):
                                    self.manager.removeGameObject(room.exitDoor)
                                if room.exitDoor != None:
                                    room.walls.remove(room.exitDoor)
                                    room.unlockDoor()
                        else:
                            for j in range(len(self.dungeon.rooms)):
                                if j == i:
                                    continue
                                for enemy in self.dungeon.rooms[j].enemies:
                                    if self.manager.hasReferenceToGameObject(enemy):
                                        self.manager.removeGameObject(enemy)
                                room = self.dungeon.rooms[j]
                                for wall in room.walls.sprites():
                                    if self.manager.hasReferenceToGameObject(wall):
                                        self.manager.removeGameObject(wall)
                if self.player.usingAbility:
                    if self.particleEmitter.currentPosition == None:
                        self.particleEmitter.setPosition(self.player)
                    if not self.particleEmitter.shouldEmit:
                        self.particleEmitter.turnOnParticles()
                    if self.player.class_name == "WIZARD":
                        self.HUD.timer += dt
                    elif self.player.class_name == "PALADIN":
                        self.player.heal_party(self.party_list)
                else:
                    if self.particleEmitter.shouldEmit:
                        self.particleEmitter.turnOffParticles()

                self.collisionHandling(dt)
                self.addProjectiles()


                if not self.player.alive:
                    prevRect = self.player.rect
                    self.manager.removeGameObject(self.player)
                    self.party_list.swapPlayer()
                    self.player = self.party_list.active_member
                    self.player.set_pos(prevRect)
                    self.manager.addGameObject(self.player)

                #Win Condition
                if not self.boss.alive:
                    self.end_boss()
                    self.gameWin()

                #Lose Conditions
                if self.outOfBounds(self.player.rect.center) or self.allPlayersDead():
                    self.gameOverCondition = "You Died!"

                if self.HUD.getTime() <=0:
                    self.gameOverCondition = "Times Up!"

                self.particleEmitter.setPosition(self.player)
                self.camera.setCameraPosition(self.player.rect.center)
                pygame.draw.rect(self.window, (255, 255, 255), self.player.rect, 2)
                self.window.fill(self.bg_color)
                self.camera.draw(self.window, self.player, self.enemiesByRoom, self.projectiles, self.particleEmitter)
                self.HUD.draw(self.window, self.party_list, dt)
            pygame.display.flip()

    def end_boss(self):
        """ Display boss defeated screen"""
        self.loading.draw(self.window, "boss")
        time.sleep(2)

    def let_player_pass(self,nextRoom):
        pass

    def player_swap_cd(self, dt):
        """ 3 second cooldown on switching
            active party member."""
        self.party_list.last_active += dt
        #print(self.party_list.last_active)

    def allPlayersDead(self):
        for player in self.party_list.party_members:
            if player.stats['CUR_HP'] > 0:
                return False
        return True

    def outOfBounds(self,playerPos):
        for room in self.camera.dungeon.rooms:
            bounds = room.bgImageRect
            if bounds.collidepoint(playerPos):
                return False
        return True

    def collisionHandling(self,dt):
        """ Move Player and Check for Collisions"""

        hasCollided = False
        for room in self.dungeon.rooms:
            if self.player.rect.colliderect(room.bgImageRect):
                hasCollided = True

                # This code causes issues, was previously calling DungeonRoom method that no longer exists, now needs to
                #  call Objective method for determine objective
                # objective = Objective.evaluateObjective()
                # self.HUD.getRoomObj(objective)
                break

        if not hasCollided:
            self.gameOver()

        currentRoomIndex = None
        roomWidth = self.dungeon.rooms[0].bgImageRect.w
        tiles = pygame.sprite.Group()

        roomIndices = []
        for i in range(len(self.dungeon.rooms)):
            if self.player.rect.colliderect(self.dungeon.rooms[i].bgImageRect):
                tiles.add(self.dungeon.rooms[i].walls.sprites())
                roomIndices.append(i)

        self.collisionCheck(tiles,dt)

        for p in self.projectiles:
            inRoom = False
            for i in roomIndices:
                if p.hitbox.colliderect(self.dungeon.rooms[i].bgImageRect):
                    inRoom = True
                    break
            if not inRoom:
                if self.manager.hasReferenceToGameObject(p):
                    self.manager.removeGameObject(p)
                    self.projectiles.remove(p)
                    continue

            for tile in tiles:
                if tile.rect.colliderect(p.hitbox):
                    if self.manager.hasReferenceToGameObject(p):
                        self.manager.removeGameObject(p)
                        self.projectiles.remove(p)

    def collisionCheck(self,tiles,dt):

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
                    if(not self.manager.hasReferenceToGameObject(enemy)):
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

                    for enemy in room.enemies:          #DEBUG
                        if self.player.rect.colliderect(enemy.rect):
                            self.player.receive_dmg(enemy.stats["MELEE"],enemy.facing_right)

                if self.player.cur_weapon is not None:
                    #print("DungeonRun.py: Line 244: ", self.player.cur_weapon.active)
                    if self.player.cur_weapon.active:
                        for enemy in room.enemies:
                            if self.player.cur_weapon.rect.colliderect(enemy.rect):
                                #print("DungeonRun.py: Line 247: ", self.player.cur_weapon.rect.colliderect(enemy.rect))
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
        self.party_list.calc_avg_level()
        self.manager.cleanup()
        self.running = False
        credits = Credits(self.manager,self.window)
        credits.start_credits()
        credits.begin_sequence()

    def gameOver(self):
        "The Player's Experience gets reset"
        self.running = False
        credits = Credits(self.manager,self.window)
        credits.start_credits()
        credits.begin_sequence()

    def getPartyReference(self):
        return self.party_list