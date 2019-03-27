import pygame
import time
from Actors.Actor import *

class Player(Actor):
    """ The player class which will be controlled
        by the user."""

    def __init__(self, start_pos, img):
        super().__init__(start_pos)
        self.playerHeight = 48
        self.level = 1
        self.alive = True
        self.t_anim = time.time() + 0.125 #timer used for animations
        self.anim = 0 #which frame of animations are active.
        self.rframes = [pygame.image.load(img + "/right1.png"),
                        pygame.image.load(img + "/right2.png"),
                        pygame.image.load(img + "/right3.png"),
                        pygame.image.load(img + "/right2.png")]
        self.frames = {"right": pygame.image.load(img + "/right1.png"),
                       "rjump": pygame.image.load(img + "/jump1.png"),}
        # dictionary of frames.  the values will be updating to make animations
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
        self.currentAbilityTimer = 0
        self.type = "PLAYER"

        # weapon dictionary with weapon name as key,
        # weapon object as value
        self.weapons = {}
        #self.cur_weapon = self.weapons["blah"]
        self.cur_weapon = None

        # figure out an exact time later
        self.invuln_timer = 0

        self.jumpFrameCount = 0
        self.jumpFrames = 2

    def basic_attack(self, mbuttons, keys, dt):
        """ Generic attack method. Will be
            overridden by more specialized
            classes later (maybe)."""
        if mbuttons[0]:
            self.cur_weapon.active = True

    def receive_dmg(self, enemy_object):
        """ Generic method for when a
            player takes damage. Can be
            overridden if need be."""
        if self.stats["CUR_HP"] > 0 >= self.invuln_timer:    # testing with this for now - Jon
            if self.stats["CUR_HP"] - enemy_object.damage <= 0:
                self.stats["CUR_HP"] = 0
                self.alive = False
            else:
                self.stats["CUR_HP"] -= enemy_object.damage
            self.invuln_timer = INVULN_TIMER

    def update(self, *args):
        """ Testing Player jumping."""
        mouseButtons, keys, dt = args

        super().update(*args)

        if self.jumpFrameCount > 0:
            self.jumpFrameCount -= 1
            self.velocity += self.jump_vector

        if keys[pygame.K_d]:
            self.facing_right = True
            self.image = self.frames["right"]
        if keys[pygame.K_a]:
            self.facing_right = False
            self.image = pygame.transform.flip((self.frames["right"]), True, False)

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

    def gain_xp(self):
        """ Generic method for gaining
            xp."""
        pass

    def gain_level(self):
        """ Generic method for increasing
            player level."""
        pass


    def healPlayer(self, health):
        if self.stats["CUR_HP"] + health >= self.stats["MAX_HP"]:
            self.stats["CUR_HP"] = self.stats["MAX_HP"]
        else:
            self.stats["CUR_HP"] += health

    def draw(self, window, cameraPos):
        super().draw(window, cameraPos)
        window.blit(self.image, (int(self.rect.x - cameraPos[0]),int(self.rect.y - cameraPos[1])))
        if self.debug:
            debug = pygame.Rect(int(self.rect.x - cameraPos[0]), int(self.rect.y - cameraPos[1]), self.rect.w, self.rect.h)
            pygame.draw.rect(window,pygame.color.THECOLORS['red'],debug,1)
        if self.cur_weapon is not None:
            if self.facing_right:
                if self.cur_weapon.active:
                        window.blit(self.cur_weapon.image,
                                    (self.rect.x - cameraPos[0] + 15, self.rect.y - cameraPos[1])
                                    )
            if not self.facing_right:
                if self.cur_weapon.active:
                        window.blit(pygame.transform.flip(self.cur_weapon.image, True, False),
                                    (self.rect.x - cameraPos[0] - 15, self.rect.y - cameraPos[1])
                                    )