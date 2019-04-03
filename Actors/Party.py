from PlayerClasses.Warrior import *
from PlayerClasses.Ranger import *
from PlayerClasses.Wizard import *
from PlayerClasses.Paladin import *
import pygame


class Party:
    """ The Party class will contain a list
        of party members, and handle which party member
        is currently active in gameplay."""
    def __init__(self, start_pos):
        # CONSTRUCTOR PARAMETERS:
        # mem1, mem2, mem3, mem4: Each one of these is an
        # individual party member

        self.party_members = [Warrior(start_pos),   #Jon is working on this
                              Ranger(start_pos),    #??
                              Wizard(start_pos),    #Mike is working on this
                              Paladin(start_pos)    #Alex is working on this
                              ]
        self.party_index = 0
        self.active_member = self.party_members[self.party_index]
        self.last_active = 3    # time in seconds
        self.wealth = None
        self.avg_level = None
        self.cur_dungeon = None

    def update(self, key, dt):
        """ Method for changing active
            party member."""

        if self.last_active > 3:

            if key == pygame.K_w:
                count = 0
                while count < len(self.party_members):
                    self.party_index -= 1
                    if self.party_index < 0:
                        self.party_index = len(self.party_members) - 1
                    if self.party_members[self.party_index].alive:
                        break
                    count += 1
                self.last_active = 0
            elif key == pygame.K_s:
                count = 0
                while count < len(self.party_members):
                    self.party_index += 1
                    if self.party_index > len(self.party_members) - 1:
                        self.party_index = 0
                    if self.party_members[self.party_index].alive:
                        break
                    count += 1
                self.last_active = 0

            elif key == pygame.K_1:
                if self.party_members[0].alive:
                    self.party_index = 0
                    self.last_active = 0
            elif key == pygame.K_2:
                if self.party_members[1].alive:
                    self.party_index = 1
                    self.last_active = 0
            elif key == pygame.K_3:
                if self.party_members[2].alive:
                    self.party_index = 2
                    self.last_active = 0
            elif key == pygame.K_4:
                if self.party_members[3].alive:
                    self.party_index = 3
                    self.last_active = 0

        self.active_member = self.party_members[self.party_index]

    def swapPlayer(self):
        count = 0
        index = self.party_index
        while not self.party_members[self.party_index].alive  and count < len(self.party_members):
            self.party_index += 1
            if self.party_index > len(self.party_members) - 1:
                self.party_index = 0
            count += 1

        self.active_member = self.party_members[self.party_index]

    def calc_avg_level(self):
        """ Method for calculating average
            level of the party."""
        for char in self.party_members:
            self.avg_level += char.level
        self.avg_level /= len(self.party_members)
