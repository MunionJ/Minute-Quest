import random
import time
from Actors.Actor import *


class Player(Actor):
    """ The player class which will be controlled
        by the user."""

    def __init__(self, start_pos, img):
        super().__init__(start_pos)
        self.playerHeight = 48
        self.class_name = ""
        self.level = 1
        self.max_level = 20
        self.cur_xp = 0
        self.xp_to_level = 1000
        self.alive = True
        self.t_anim = time.time() + 0.125 #timer used for animations
        self.anim = 0 #which frame of animations are active.
        self.rframes = [pygame.image.load(img + "/right1.png"),
                        pygame.image.load(img + "/right2.png"),
                        pygame.image.load(img + "/right3.png"),
                        pygame.image.load(img + "/right2.png")]
        #self.swingframes = [pygame.image.load(img + "/swing1.png")]
        self.frames = {"right": pygame.image.load(img + "/right1.png"),
                       "rjump": pygame.image.load(img + "/jump1.png"),}

        # dictionary of frames.  the values will be updating to make animations
        #for i in self.swingframes:
        #    rect = self.swingframes[i].get_rect()
        #    width = int(rect.w*(self.playerHeight/rect.h))
        #    height = self.playerHeight
        #    self.swingframes[i] = pygame.transform.scale(self.swingframes[i], (width, height))
        #    self.swingframes[i] = self.swingframes[i].convert_alpha()
        for i in self.frames:
            rect = self.frames[i].get_rect()
            width = int(rect.w*(self.playerHeight/rect.h))
            height = self.playerHeight
            self.frames[i] = pygame.transform.scale(self.frames[i], (width, height))
            self.frames[i] = self.frames[i].convert_alpha()
        for i in range(len(self.rframes)):
            rect = self.rframes[i].get_rect()
            width = int(rect.w*(self.playerHeight/rect.h))
            height = self.playerHeight
            self.rframes[i] = pygame.transform.scale(self.rframes[i], (width, height))
            self.rframes[i] = self.rframes[i].convert_alpha()
        self.rect = self.frames["right"].get_rect()
        self.image = self.frames["right"]
        self.facing_right = True
        self.usingAbility = False
        self.abilityCoolDown = 5
        self.currentAbilityTimer = 5
        self.type = "PLAYER"
        self.is_seen = False
        self.swing_time = 0
        self.swing_cooldown = 2
        # weapon dictionary with weapon name as key,
        # weapon object as value
        self.weapons = {}
        #self.cur_weapon = self.weapons["blah"]
        self.cur_weapon = None

        # figure out an exact time later
        self.invuln_timer = 0

        self.most_recent_dmg = 0
        self.dmg_display_timer = 0
        self.dmg_display_max_time = 0.8
        self.dmg_display_y_offset = 0

        self.jumpFrameCount = 0
        self.jumpFrames = 2
        self.camera_offset = None
        self.weapon_cords = (0,0)
        self.attack_duration = 500 #this should make the attack animation happen faster at lower numbers but it also increases the degrees rotated.

    def basic_attack(self, mbuttons, keys, dt):
        """ Generic attack method. Will be
            overridden by more specialized
            classes later (maybe)."""
        if self.class_name != "RANGER":
            self.weapon_rotated = pygame.transform.rotate(self.cur_weapon.image,
                                                      45 - ((pygame.time.get_ticks() - self.swing_time) / self.attack_duration) * 160)
        if pygame.time.get_ticks() - self.attack_duration > self.swing_time:
            self.cur_weapon.active = False
        if mbuttons[0]:
            if pygame.time.get_ticks() - self.attack_duration > self.swing_time:
               # if self.facing_right:
               #     self.image = self.swingframes[0]
               # if not self.facing_right:
               #     self.image = pygame.transform.flip(self.swingframes[0], True, False)
                self.cur_weapon.active = True
                self.swing_time = pygame.time.get_ticks()

    def receive_dmg(self, enemy_object):
        """ Generic method for when a
            player takes damage. Can be
            overridden if need be."""
        self.most_recent_dmg = enemy_object.stats["MELEE"]
        if self.stats["CUR_HP"] > 0 >= self.invuln_timer:    # testing with this for now - Jon
            if self.stats["CUR_HP"] - enemy_object.stats["MELEE"] <= 0:
                self.stats["CUR_HP"] = 0
                self.alive = False
            else:
                self.stats["CUR_HP"] -= enemy_object.stats["MELEE"]
                self.receive_knockback(enemy_object)
            self.invuln_timer = INVULN_TIMER

    def receive_knockback(self, enemy_object):
        if enemy_object.facing_right is True:
            x = random.randint(30, 50)
        else:
            x = random.randint(-50, -30)
        if self.cur_state == states.Jumping:
            y = 0
        else:
            y = random.randint(-20, -15)
        self.velocity += pygame.math.Vector2(x, y)

    def update(self, *args):
        """ Testing Player jumping."""
        mouseButtons, keys, dt, projectiles = args

        super().update(*args)

        if self.jumpFrameCount > 0:
            self.jumpFrameCount -= 1
            self.velocity += self.jump_vector

        if keys[pygame.K_d]:
            self.facing_right = True
            self.image = self.frames["right"]
            if self.cur_weapon is not None:
                self.cur_weapon.rect.bottomleft = self.rect.center

        if keys[pygame.K_a]:
            self.facing_right = False
            self.image = pygame.transform.flip((self.frames["right"]), True, False)
            if self.cur_weapon is not None:
                self.cur_weapon.rect.bottomright = self.rect.center

        if keys[pygame.K_SPACE] and (self.cur_state == states.Standing or self.cur_state == states.Running):
            self.jump()

        while time.time() > self.t_anim:
            self.anim += 1
            if self.anim > len(self.rframes)-1:
                self.anim = 0
            self.frames["right"] = self.rframes[self.anim]
            self.t_anim = time.time() + 0.25

        if self.cur_state == states.Jumping or self.cur_state == states.Falling:
            if self.facing_right:
                self.image = self.frames["rjump"]
            if not self.facing_right:
                self.image = pygame.transform.flip(self.frames['rjump'], True, False)

        self.invuln_timer -= dt

    def isInAir(self):
        if self.jumpFrameCount <= 0:
            super().isInAir()

    def determineState(self):
        # TODO Fix determine state in this file
        if not self.onSurface and self.jumpFrameCount <= 0:
            self.changeState(states.Falling)
            return

        if self.velocity.y > 0:
            self.changeState(states.Falling)
            return

        if self.velocity.y < 0:
            self.changeState(states.Jumping)
            return

        if self.cur_state != states.Jumping or self.cur_state != states.Falling:
            if self.velocity.x != 0:
                self.changeState(states.Running)
                return
            elif self.onSurface:
                self.changeState(states.Standing)
                return

    def move(self, keys, dt):
        movedHorizontal = False
        if keys[pygame.K_s]:
            # Implement ability to crouch?
            pass
        if keys[pygame.K_d]:
            if self.accel.x < MAX_X_ACC:
                self.accel.x += PLAYER_ACC
            movedHorizontal = True
        if keys[pygame.K_a]:
            if self.accel.x > -MAX_X_ACC:
                self.accel.x -= PLAYER_ACC
            movedHorizontal = True

        if keys[pygame.K_F1]:
            self.debug = not self.debug

        # if the entity is not currently moving, decrease their velocity until it reaches 0
        if not keys[pygame.K_a]:
            if self.accel.x < 0:
                self.accel.x = 0
            if self.velocity.x < 0:
                self.velocity.x -= 2*PLAYER_FRICTION
                if self.velocity.x > 0:
                    self.velocity.x = 0
        if not keys[pygame.K_d]:
            if self.accel.x > 0:
                self.accel.x = 0
            if self.velocity.x > 0:
                self.velocity.x += 2*PLAYER_FRICTION
                if self.velocity.x < 0:
                    self.velocity.x = 0


    def jump(self):
        """ Generic jump method. Can be
            overridden later."""

        if self.facing_right:
            self.image = self.frames["rjump"]
        if not self.facing_right:
            self.image = pygame.transform.flip(self.frames['rjump'], True, False)
        if self.onSurface:
            self.velocity += self.jump_vector
            self.jumpFrameCount = self.jumpFrames

    def use_ability(self):
        """ Generic ability usage class.
            Can be overriden later."""
        self.usingAbility = True

    def end_ability(self):
        """ Signal to game that the player has finished using their ability"""
        self.usingAbility = False

    def use_item(self):
        """ Generic item usage method.
            Maybe relocate it to Party class
            later?"""
        pass

    def set_dead(self):
        """ Generic method for setting
            a Player status to dead."""
        self.alive = False

    def gain_xp(self, enemy_obj, multiplier=1):
        """ Generic method for gaining
            xp."""
        # xp gain formula: enemy base xp value * (enemy level / player level)
        self.cur_xp += (enemy_obj.xp_value * (enemy_obj.level / self.level)) * multiplier
        while self.cur_xp >= self.xp_to_level:
            self.gain_level()
            self.cur_xp -= self.xp_to_level

    def gain_level(self):
        """ Generic method for increasing
            player level."""
        self.level += 1


    def healPlayer(self, health):
        if self.stats["CUR_HP"] + health >= self.stats["MAX_HP"]:
            self.stats["CUR_HP"] = self.stats["MAX_HP"]
        else:
            self.stats["CUR_HP"] += health

    def display_damage(self, window, cameraPos):
        """ Method for displaying damage numbers when
            a Player takes damage.
        """
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
        self.camera_offset = cameraPos
        window.blit(self.image, (int(self.rect.x - cameraPos[0]),int(self.rect.y - cameraPos[1])))
        if self.debug:
            debug = pygame.Rect(int(self.rect.x - cameraPos[0]), int(self.rect.y - cameraPos[1]), self.rect.w, self.rect.h)
            pygame.draw.rect(window, pygame.color.THECOLORS['red'], debug, 1)
        if self.cur_weapon is not None:
            if self.facing_right:
                if self.cur_weapon.active:
                        window.blit(self.weapon_rotated,
                                    (self.rect.x - cameraPos[0] + 10, self.rect.y - cameraPos[1] - 10 + ((pygame.time.get_ticks() - self.swing_time) / self.attack_duration) * 23)
                                    # this moves the y cord of the weapon as it rotates. hacky way to match rotation. doesnt really work.
                                    )

                        # pygame.draw.rect(window,
                        #                  (255, 0, 0),
                        #                  (self.cur_weapon.rect.x - cameraPos[0] + 25,
                        #                   self.cur_weapon.rect.y - cameraPos[1],
                        #                   self.cur_weapon.rect.w,
                        #                   self.cur_weapon.rect.h
                        #                   ),
                        #                  2)
            if not self.facing_right:
                if self.cur_weapon.active:
                        window.blit((pygame.transform.flip(self.weapon_rotated, True, False)),
                                    (self.rect.x - cameraPos[0]-20, self.rect.y - cameraPos[1] - 10 + ((pygame.time.get_ticks() - self.swing_time) / self.attack_duration) * 23))


                        # pygame.draw.rect(window,
                        #                  (255, 0, 0),
                        #                  (self.cur_weapon.rect.x - cameraPos[0] - 25,
                        #                   self.cur_weapon.rect.y - cameraPos[1],
                        #                   self.cur_weapon.rect.w,
                        #                   self.cur_weapon.rect.h
                        #                   ),
                        #                  2)
        self.display_damage(window, cameraPos)
