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

        if keys[pygame.K_SPACE] and self.cur_state != self.states[1] and self.jump_offset == 0:
            self.cur_state = self.states[1]

    def jump(self):
        """ Generic jump method. Can be
            overridden later."""
        if self.cur_state == self.states[1]:
            self.jump_offset += 1
            if self.jump_offset >= JUMP_HEIGHT:
                self.cur_state = self.states[3]
        elif self.jump_offset > 0 and self.cur_state == self.states[3]:
            self.jump_offset -= 1

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

    def set_pos(self):
        """ Sets the player's position."""
        self.pos = self.rect.center

