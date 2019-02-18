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

    def receive_dmg(self):
        """ Generic method for when a
            player takes damage. Can be
            overridden if need be."""
        pass

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
