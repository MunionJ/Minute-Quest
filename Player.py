import pygame
import time
from Actor import *


class Player(Actor):
    """ The player class which will be controlled
        by the user."""

    def __init__(self, start_pos, img):
        super().__init__(start_pos)
        self.level = 1
        self.alive = True
        self.t_anim = time.time() + 1 #timer used for animations
        self.anim = 0 #which frame animations are on. player move animations that update need same number of frames currently
        self.lframes = [ pygame.transform.flip(pygame.image.load(img + "/right1.png"), True, False),
                         pygame.transform.flip(pygame.image.load(img + "/right2.png"), True, False),
                         pygame.transform.flip(pygame.image.load(img + "/right3.png"), True, False),
                         pygame.transform.flip(pygame.image.load(img + "/right2.png"), True, False)]
        # list of frames while moveing right.
        self.rframes = [pygame.image.load(img + "/right1.png"),
                        pygame.image.load(img + "/right2.png"),
                        pygame.image.load(img + "/right3.png"),
                        pygame.image.load(img + "/right2.png")]
        self.frames = {"right" : pygame.image.load(img + "/right1.png"),
                       "left" : pygame.transform.flip(pygame.image.load(img + "/right1.png"), True, False),
                       "rjump" : pygame.image.load(img + "/jump1.png"),
                       "ljump": pygame.transform.flip(pygame.image.load(img + "/jump1.png"), True, False), }
        # dictionary of frames.  the values will be updating to make animations
        for i in self.frames:
            rect = self.frames[i].get_rect()
            width = int(rect.w*(64/rect.h))
            height = 64
            self.frames[i] = pygame.transform.scale(self.frames[i], (width, height))
            self.frames[i] = self.frames[i].convert_alpha()
        for i in range(len(self.lframes)):
            rect = self.lframes[i].get_rect()
            width = int(rect.w*(64/rect.h))
            height = 64
            self.lframes[i] = pygame.transform.scale(self.lframes[i], (width, height))
            self.lframes[i] = self.lframes[i].convert_alpha()
        for i in range(len(self.lframes)):
            rect = self.lframes[i].get_rect()
            width = int(rect.w*(64/rect.h))
            height = 64
            self.rframes[i] = pygame.transform.scale(self.rframes[i], (width, height))
            self.rframes[i] = self.rframes[i].convert_alpha()
        self.rect = self.frames["right"].get_rect()
        self.image = self.frames["right"]

        # weapon dictionary with weapon name as key,
        # weapon sprite as value
        self.weapons = {}
        #self.cur_weapon = self.weapons["blah"]
        # figure out a time later
        self.invuln_timer = 3

        # pass a list as constructor parameter to specialized character class to set defaults
        self.stats = {
            "MELEE": 0,
            "RANGE": 0,
            "MAGIC": 0,
            "CUR_HP": 0,
            "MAX_HP": 0
        }

    def melee_attack(self):
        """ Generic melee attack method. Will be
            overridden by more specialized
            classes later."""
        pass

    def ranged_attack(self):
        """ Generic ranged attack method. Blah blah blah."""
        pass

    def receive_dmg(self):
        """ Generic method for when a
            player takes damage. Can be
            overridden if need be."""
        pass

    def update(self, keys, dt):
        """ Testing Player jumping."""
        super().update(keys, dt)

        if keys[pygame.K_d]:
            self.image = self.frames["right"]
        if keys[pygame.K_a]:
            self.image = self.frames["left"]

        if keys[pygame.K_SPACE] and self.cur_state != self.states[1]:
            self.cur_state = self.states[1]
            if self.image == self.frames["right"] or self.image == self.frames["rjump"]:
                self.image = self.frames["rjump"]
            if self.image == self.frames["left"] or self.image == self.frames["ljump"]:
                self.image = self.frames["ljump"]

        while time.time() > self.t_anim:
            self.anim += 1
            if self.anim > len(self.rframes)-1:
                self.anim = 0
            self.frames["right"] = self.rframes[self.anim]
            self.frames["left"] = self.lframes[self.anim]
            self.t_anim = time.time() + 0.25





    def move(self, keys, dt):
        # print(keys[pygame.K_s], keys[pygame.K_a], keys[pygame.K_d])
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
        if movedHorizontal:
            self.cur_state = self.states[2]     # running
            self.prevPos = self.pos

            # self.velocity.length() returns the Euclidean length of the vector
            if self.velocity.length() > self.max_speed:
                self.velocity.scale_to_length(self.max_speed)

            self.pos += self.velocity
            self.rect.center = (int(self.pos.x), int(self.pos.y))

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
        pass

    def use_ability(self):
        """ Generic ability usage class.
            Can be overriden later."""
        pass

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

    def draw(self, window):
        super().draw(window)
        window.blit(self.image, self.rect)
