from Actors.Actor import Actor
import pygame
import time
import math
import random
from Actors.PlayerStates import PlayerStates as states
from config import *
from Projectiles.Arrow import Arrow

vec = pygame.math.Vector2
class Boss(Actor):

        def __init__(self, spawn_point, img, xp_val=200, lvl=1):
            super().__init__(spawn_point)
            self.enemyHeight = 94
            self.level = lvl
            self.xp_value = xp_val
            self.alive = True
            self.t_anim = 125  # timer used for animations
            self.anim = 0  # which frame of animations are active.
            self.rframes = [pygame.image.load(img + "/right1.png"),
                            pygame.image.load(img + "/right2.png"),
                            pygame.image.load(img + "/right3.png"),
                            pygame.image.load(img + "/right4.png")]
            self.frames = {"right": pygame.image.load(img + "/right1.png"),
                           "rjump": pygame.image.load(img + "/jump1.png"), }
            # dictionary of frames.  the values will be updating to make animations
            for i in self.frames:
                rect = self.frames[i].get_rect()
                width = int(rect.w * (self.enemyHeight / rect.h))
                height = self.enemyHeight
                self.frames[i] = pygame.transform.scale(self.frames[i], (width, height))
                self.frames[i] = self.frames[i].convert_alpha()
            for i in range(len(self.rframes)):
                rect = self.rframes[i].get_rect()
                width = int(rect.w * (self.enemyHeight / rect.h))
                height = self.enemyHeight
                self.rframes[i] = pygame.transform.scale(self.rframes[i], (width, height))
                self.rframes[i] = self.rframes[i].convert_alpha()
            self.rect = self.frames["right"].get_rect()
            self.img = self.frames["right"]
            self.facing_right = True
            self.jumpFrameCount = 0
            self.jumpFrames = 2
            self.move_time = time.time() + 2  # temporary variable for moving enemies
            self.change_move = True  # temporary variable for moving enemies
            self.rect = self.img.get_rect()
            self.rect.midbottom = spawn_point
            self.pos.x, self.pos.y = self.rect.center
            self.alive = True
            self.cur_state = states.Falling
            self.onSurface = True
            self.stats["MAX_HP"] = 20 * self.level
            self.stats["CUR_HP"] = self.stats["MAX_HP"]
            self.stats["MELEE"] = 3
            self.stats["RANGE"] = 3
            self.stats["MAGIC"] = 3
            for i in range(self.level):
                self.stats["MELEE"] += random.randint(1, 2)
                self.stats["RANGE"] += random.randint(1, 2)
                self.stats["MAGIC"] += random.randint(1, 2)
            self.invuln_timer = 0
            self.type = "ENEMY"
            self.sees_player = False
            self.shouldJump = False
            self.vision_range = 400
            self.now = pygame.time.get_ticks()
            self.target_vector = None
            self.hitWall = False
            self.rocks_fell = False
            self.cycle_projectiles = 30
            self.projectile_Cooldown = 2
            self.last_summon = 0
            self.direction_timer = 0
            self.direction_cooldown = 4

        def move(self, keys, dt):  # TODO: ADJUST THIS TO WORK IN AN EXPECTED MANNER

            if self.sees_player:
                if self.shouldJump:
                    self.jump()
                    self.shouldJump = False

                #if self.facing_right:
                #    self.accel.x += ENEMY_ACC * dt
                #else:
                #    self.accel.x -= ENEMY_ACC * dt

                if self.accel.length() > MAX_ACC:
                    self.accel.scale_to_length(MAX_ACC)

                self.velocity += self.accel

                if self.velocity.length() > ENEMY_MAX_VEL:
                    self.velocity.scale_to_length(ENEMY_MAX_VEL)


            else:
                # self.facing_right = True
                self.accel = vec(0, 0)
                self.velocity = vec(0, self.velocity.y)

        def jump(self):
            """ Generic jump method. Can be
                overridden later."""

            if self.facing_right:
                self.img = self.frames["rjump"]
            if not self.facing_right:
                self.img = pygame.transform.flip(self.frames['rjump'], True, False)
            if self.onSurface:
                self.velocity += 1.5 * self.jump_vector
                self.jumpFrameCount = self.jumpFrames

        def determineState(self):
            if self.velocity.x < 0:
                self.facing_right = False
                self.img = pygame.transform.flip(self.frames["right"], True, False)

            if self.velocity.x > 0:
                self.facing_right = True
                self.img = self.frames["right"]

            if self.velocity.y > 0:
                self.changeState(states.Falling)

            if self.velocity.y < 0:
                self.changeState(states.Jumping)

            if self.cur_state != states.Jumping or self.cur_state != states.Falling:
                if self.velocity.x != 0:
                    self.changeState(states.Running)
                else:
                    self.changeState(states.Standing)

            if self.onSurface:
                if self.velocity.x != 0:
                    self.changeState(states.Running)
                else:
                    self.changeState(states.Standing)


            if not self.onSurface:
                self.changeState(states.Falling)

        def update(self, *args):
            mouseButtons, keys, dt, projectiles = args
            self.apply_physics(dt)

            self.move(keys, dt)
            if self.stats["CUR_HP"] >= 0.5*self.stats["MAX_HP"]:
                self.stage_one_tactics(dt,projectiles)
            self.invuln_timer -= dt

            while time.time() > self.t_anim:
                self.anim += 1
                if self.anim > len(self.rframes) - 1:
                    self.anim = 0
                self.frames["right"] = self.rframes[self.anim]
                self.t_anim = time.time() + 0.25

            self.projectile_Cooldown -= dt
            self.direction_timer -= dt
            if self.hitWall:
                self.direction_timer = 0

        def set_dead(self):
            """ Generic method for setting
                a enemy status to dead."""
            self.alive = False

        def line_of_sight(self, window, cameraPos, player, wallTiles):
            # for tile in wallTiles:

            # self.line = pygame.draw.line(window, (255, 255, 0), (int(self.rect.x - cameraPos[0]), int(self.rect.y - cameraPos[1])),
            #                                     (int(player.rect.x - cameraPos[0]), int(player.rect.y - cameraPos[1])))
            #     enex = int(self.rect.x - cameraPos[0])
            #     eney = int(self.rect.y - cameraPos[1])
            #     playx = int(player.rect.x - cameraPos[0])
            #     playy = int(player.rect.y - cameraPos[1])
            #     if ((enex-playx)**2) + ((eney-playy)**2) >= 150**2:
            #         vision_collision = False
            #         break
            #     if (enex - playx) == 0:
            #         vision_collision = False
            #         break
            #     lineSlope = (eney - playy)/(enex - playx)
            #     yintercept = eney+lineSlope*enex
            #
            #     v1 = tile.rect.topleft
            #     v2 = tile.rect.topright
            #     v3 = tile.rect.bottomleft
            #     v4 = tile.rect.bottomright
            #     # pygame.display.flip()
            #
            #     if (v1[0]*lineSlope+yintercept) - v1[1] > 0 and v2[0]*lineSlope+yintercept - v2[1] > 0 and v3[0]*lineSlope+yintercept - v3[1] > 0 and v4[0]*lineSlope+yintercept - v4[1] > 0 or v1[0] * lineSlope + yintercept  - v1[1] < 0 and v2[0] * lineSlope + yintercept - v2[1] < 0 and v3[0] * lineSlope + yintercept - v3[1] < 0 and v4[0] * lineSlope + yintercept  - v4[1] < 0:
            #         vision_collision = True
            #         if int((player.rect.x - cameraPos[0])) > (int(self.rect.x - cameraPos[0])):
            #             self.facing_right = True
            #         if int((player.rect.x - cameraPos[0])) < (int(self.rect.x - cameraPos[0])):
            #             self.facing_right = False
            #     else:
            #         vision_collision = False
            #         break
            # self.sees_player = vision_collision

            # v1 = tile.rect.topleft
            # v2 = tile.rect.topright
            # v3 = tile.rect.bottomleft
            # v4 = tile.rect.bottomright

            # TODO Figure a way to draw without this flip, this flip stacks with the flip in the main loop causing a
            # double flip, this is the source of the lag
            # pygame.display.flip()
            #  startx, starty = self.rect.center
            #
            #  line1 = pygame.draw.line(window, (255, 255, 0), (int(self.rect.x - cameraPos[0]), int(self.rect.y - cameraPos[1])),
            #                                      (int(v1[0] - cameraPos[0]), int(v1[1] - cameraPos[1])))
            #  line2 = pygame.draw.line(window, (255, 255, 0), (int(self.rect.x - cameraPos[0]), int(self.rect.y - cameraPos[1])),
            #                                      (int(v2[0] - cameraPos[0]), int(v2[1] - cameraPos[1])))
            #  line3 = pygame.draw.line(window, (255, 255, 0), (int(self.rect.x - cameraPos[0]), int(self.rect.y - cameraPos[1])),
            #                                      (int(v3[0] - cameraPos[0]), int(v3[1] - cameraPos[1])))
            #  line4 = pygame.draw.line(window, (255, 255, 0), (int(self.rect.x - cameraPos[0]), int(self.rect.y - cameraPos[1])),
            #                                      (int(v4[0] - cameraPos[0]), int(v4[1] - cameraPos[1])))

            #     if (v1[0] * lineSlope + yintercept) - v1[1] > 0 and v2[0] * lineSlope + yintercept - v2[1] > 0 and v3[
            #         0] * lineSlope + yintercept - v3[1] > 0 and v4[0] * lineSlope + yintercept - v4[1] > 0 or v1[
            #         0] * lineSlope + yintercept - v1[1] < 0 and v2[0] * lineSlope + yintercept - v2[1] < 0 and v3[
            #         0] * lineSlope + yintercept - v3[1] < 0 and v4[0] * lineSlope + yintercept - v4[1] < 0:
            #         vision_collision = True
            #         player.is_seen = True
            #         if int((player.rect.x - cameraPos[0])) > (int(self.rect.x - cameraPos[0])):
            #             self.facing_right = True
            #         if int((player.rect.x - cameraPos[0])) < (int(self.rect.x - cameraPos[0])):
            #             self.facing_right = False
            #     else:
            #         vision_collision = False
            #         player.is_seen = False
            #         break
            #
            # self.sees_player = vision_collision

            startX, startY = self.rect.midtop
            endX, endY = player.rect.center
            distCheck = vec(endX - startX, endY - startY)
            if distCheck.length() > self.vision_range:
                self.sees_player = False
                return

            dx = endX - startX
            dy = endY - startY
            heading = math.atan2(dy, dx)
            heading %= 2 * math.pi
            point = pygame.Rect(startX, startY, 1, 1)
            # print("In Enemies: ",math.degrees(heading),math.cos(heading),math.sin(heading))
            start = vec(self.rect.midtop[0], self.rect.midtop[1])
            tile = wallTiles.sprites()[0]
            halfdist = tile.rect.w >> 2
            dir = vec(halfdist * math.cos(heading), halfdist * math.sin(heading))
            self.target_vector = dir
            detecting = True
            count = 0
            while count < self.vision_range:
                start += dir
                point.x = int(start.x)
                point.y = int(start.y)

                if player.rect.colliderect(point):
                    self.sees_player = True
                    detecting = False
                else:
                    for tile in wallTiles:
                        if point.colliderect(tile.rect):
                            self.sees_player = False
                            detecting = False
                            break

                if not detecting:
                    break;
                count += 1

            #    pygame.draw.rect(window, pygame.color.THECOLORS['gold'],  # DEBUG
            #                     (int(point.x - cameraPos[0]), int(point.y - cameraPos[1]), 1, 1)
            #                     )
            #pygame.display.update()

            if self.sees_player:
                if player.pos.x < self.pos.x:
                    self.facing_right = False
                else:
                    self.facing_right = True

        def take_damage(self, player):
            """Method that make the enemy take damage from an attack"""
            if self.stats["CUR_HP"] > 0 and self.invuln_timer <= 0:
                if self.stats["CUR_HP"] - player.deal_dmg() <= 0:
                    self.stats["CUR_HP"] = 0
                    self.set_dead()
                else:
                    self.stats["CUR_HP"] -= player.deal_dmg()
                self.invuln_timer = INVULN_TIMER

        def attack(self):
            """Method allows the enemy attack the player when in close enough range"""
            pass

        def display_info(self, window):
            """ Method for displaying info about the Boss
                (HP bar, Level, etc.)
            """
            if self.alive:
                font = pygame.font.Font("./fonts/LuckiestGuy-Regular.ttf", 30)
                hp_surf = font.render(str(self.stats["CUR_HP"]) + " / " + str(self.stats["MAX_HP"]),
                                      False,
                                      pygame.color.THECOLORS['white']
                                      )
                level_surf = font.render("LEVEL: " + str(self.level),
                                         False,
                                         pygame.color.THECOLORS['white']
                                         )
                bar_width = 400
                bar_height = 30
                bar_x = window.get_width() // 3
                bar_y = window.get_height() - 80
                hp_bar_outline = pygame.Rect(bar_x,
                                             bar_y,
                                             bar_width,
                                             bar_height)
                hp_bar = pygame.Rect(bar_x,
                                     bar_y,
                                     (self.stats["CUR_HP"] / self.stats["MAX_HP"]) * bar_width,
                                     bar_height)
                pygame.draw.rect(window, pygame.color.THECOLORS['red'], hp_bar)
                pygame.draw.rect(window, pygame.color.THECOLORS['white'], hp_bar_outline, 2)
                window.blit(hp_surf, (bar_x + (bar_width / 2.5), bar_y + (bar_height / 5)))
                window.blit(level_surf, ((bar_x + (bar_width - 100)), bar_y - 20))

        def draw(self, window, cameraPos):
            super().draw(window, cameraPos)
            window.blit(self.img, (int(self.rect.x - cameraPos[0]), int(self.rect.y - cameraPos[1])))
            self.display_info(window)

        def stage_one_tactics(self, dt, projectiles):
            if self.target_vector != None:
                if self.target_vector.x < 0:
                    self.accel.x -= ENEMY_ACC * dt
                else:
                    self.accel.x += ENEMY_ACC * dt


            #falling rocks logic. only works once currently.
            if self.hitWall:
                if self.last_summon <= 0:
                    self.last_summon = self.projectile_Cooldown
                    for i in range(30):
                        tX = random.randint(32, 3200)
                        tY = 0
                        p = Arrow('images/Weapons/arrow.png', 32, 32, (tX,tY), (tX, 800), 0)
                        projectiles.append(p)
                    self.hitWall = False









        def handleXCollision(self, other_rect):
            if self.velocity.x > 0:
                if self.rect.left < other_rect.right:
                    self.hitWall = True
                    self.rect.right = other_rect.left
                    self.hitVerticalWall()
                    self.hitWall = True
            elif self.velocity.x < 0:
                if self.rect.right > other_rect.left:
                    self.hitWall = True
                    self.rect.left = other_rect.right
                    self.hitVerticalWall()
                    self.hitWall = True