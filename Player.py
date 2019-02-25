import pygame
from Actor import *


class Player(Actor):
    """ The player class which will be controlled
        by the user."""

    def __init__(self, start_pos, img):
        super().__init__(start_pos, img)
        self.max_hp = 10
        self.cur_hp = self.max_hp
        self.alive = True
        self.image = pygame.image.load(img)
        # need jump vector
        # weapon dictionary with weapon name as key,
        # weapon sprite as value
        self.weapons = {}
        #self.cur_weapon = self.weapons["blah"]
        # figure out a time later
        self.invuln_timer = 3
        # player stats: a dictionary or a Stats class?


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
        # print(self.pos, self.rect.center)

        if keys[pygame.K_SPACE] and self.cur_state != self.states[1]:
            self.cur_state = self.states[1]

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

    def set_pos(self, new_rect):
        """ Sets the player's position."""
        if int(self.rect[0]) != int(new_rect[0]):
            self.rect[0] = new_rect[0]
            self.velocity.x = 0
            self.accel.x = 0
            self.pos.x = self.rect.center[0]
        if int(self.rect[1]) != int(new_rect[1]):
            self.rect[1] = new_rect[1]
            self.velocity.y = 0
            self.accel.y = 0
            self.pos.y = self.rect.center[1]
        print(self.pos, self.velocity, self.accel)
