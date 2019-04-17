from Actors.Actor import *
import time
import math
import random

vec = pygame.math.Vector2


class Enemy(Actor):
    """Basic enemy class that creates the properties/methods shared across all enemies."""

    def __init__(self, spawn_point, img, xp_val=100, lvl=1):
        super().__init__(spawn_point)
        self.enemyHeight = 48
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
        self.stats["MAX_HP"] = 7 * self.level
        self.stats["CUR_HP"] = self.stats["MAX_HP"]
        self.stats["MELEE"] = 3
        for i in range(self.level):
            self.stats["MELEE"] += random.randint(0, 1)
        self.invuln_timer = 0
        self.type = "ENEMY"
        self.sees_player = False
        self.shouldJump = False
        self.vision_range = 250
        self.most_recent_dmg = 0
        self.dmg_display_timer = 0
        self.dmg_display_max_time = 0.8
        self.dmg_display_y_offset = 0
        self.now = pygame.time.get_ticks()

    def move(self, keys, dt):  # TODO: ADJUST THIS TO WORK IN AN EXPECTED MANNER

        if self.sees_player:
            if self.shouldJump:
                self.jump()
                self.shouldJump = False

            if self.facing_right:
                self.accel.x += ENEMY_ACC * dt
            else:
                self.accel.x -= ENEMY_ACC * dt

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
            self.image = self.frames["rjump"]
        if not self.facing_right:
            self.image = pygame.transform.flip(self.frames['rjump'], True, False)
        if self.onSurface:
            self.velocity += 1.5 * self.jump_vector
            self.jumpFrameCount = self.jumpFrames

    def determineState(self):
        if self.velocity.x < 0:
            self.facing_right = False

        if self.velocity.x > 0:
            self.facing_right = True

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

        while time.time() > self.t_anim:
            self.anim += 1
            if self.anim > len(self.rframes) - 1:
                self.anim = 0
            self.frames["right"] = self.rframes[self.anim]
            self.t_anim = time.time() + 0.25

        if self.cur_state == states.Standing and self.facing_right:
            self.img = self.rframes[0]
        if self.cur_state == states.Standing and not self.facing_right:
            self.img = pygame.transform.flip(self.frames['right'], True, False)
        if self.cur_state == states.Running and self.facing_right:
            self.img = self.rframes[self.anim]
        if self.cur_state == states.Running and not self.facing_right:
            self.img = pygame.transform.flip(self.rframes[self.anim], True, False)

        self.move(keys, dt)

        self.invuln_timer -= dt

    def set_dead(self):
        """ Generic method for setting
            a enemy status to dead."""
        self.alive = False

    def line_of_sight(self, window, cameraPos, player, wallTiles):

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

        #     pygame.draw.rect(window,pygame.color.THECOLORS['gold'],                   #DEBUG
        #          (int(point.x - cameraPos[0]),int(point.y - cameraPos[1]),1,1)
        #                  )
        # pygame.display.update()

        if self.sees_player:
            if player.pos.x < self.pos.x:
                self.facing_right = False
            else:
                self.facing_right = True

            if player.pos.y < self.pos.y:
                self.shouldJump = True
            else:
                self.shouldJump = False

    def take_damage(self, player):
        """Method that make the enemy take damage from an attack"""
        damage = player.deal_dmg()
        if self.stats["CUR_HP"] > 0 and  self.invuln_timer <= 0:
            if self.stats["CUR_HP"] - damage <= 0:
                self.stats["CUR_HP"] = 0
                self.set_dead()
            else:
                self.stats["CUR_HP"] -= damage
                self.most_recent_dmg = damage
            self.invuln_timer = INVULN_TIMER

    def attack(self):
        """Method allows the enemy attack the player when in close enough range"""
        pass

    def display_damage(self, window, cameraPos):
        if self.most_recent_dmg > 0:
            if self.dmg_display_timer < self.dmg_display_max_time:
                dt = 0.016
                self.dmg_display_timer += dt
                font = pygame.font.Font("./fonts/LuckiestGuy-Regular.ttf", 32)
                surf = font.render(str(self.most_recent_dmg),
                                   False,
                                   pygame.color.THECOLORS['white']
                                   )
                window.blit(surf,
                            (int(self.rect.x - cameraPos[0] + 10), int(self.rect.y - cameraPos[1] - self.dmg_display_y_offset)))
                self.dmg_display_y_offset += 2
            else:
                self.most_recent_dmg = 0
                self.dmg_display_timer = 0
                self.dmg_display_y_offset = 0

    def draw(self, window, cameraPos):
        super().draw(window, cameraPos)
        window.blit(self.img, (int(self.rect.x - cameraPos[0]), int(self.rect.y - cameraPos[1])))
        self.display_damage(window, cameraPos)
