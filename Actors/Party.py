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
                              Wizard(start_pos),    #Daniel is working on this
                              Paladin(start_pos)    #Alex is working on this
                              ]
        self.party_index = 0
        self.active_member = self.party_members[self.party_index]
        self.last_active = 3    # time in seconds
        self.wealth = None
        self.avg_level = 1
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

    def award_xp(self, enemy_list):
        """ Method for distributing xp to the party."""
        for enemy in enemy_list:
            for member in self.party_members:
                if member.alive:
                    if self.active_member == member:
                        member.gain_xp(enemy, 1.25)
                    else:
                        member.gain_xp(enemy)

    def calc_avg_level(self):
        """ Method for calculating average
            level of the party."""
        for char in self.party_members:
            self.avg_level += char.level
        self.avg_level /= len(self.party_members)
        self.avg_level = int(self.avg_level)

    def partyInfoToPickle(self):
        partyMemberInfo = []
        for member in self.party_members:
            info ={}
            info['level'] = member.level
            info['stats'] = member.stats
            info['xp'] = member.cur_xp
            partyMemberInfo.append(info)

        retData = {
            'partyMembers': partyMemberInfo,
            'partyIndex': self.party_index,
            'avg_level': self.avg_level,
        }

        return retData

    def loadPartyInfoFromSave(self,data):
        partyInfo = data['partyMembers']
        for i in range(len(self.party_members)):
            info = data['partyMembers'][i]
            member = self.party_members[i]
            member.level = info['level']
            member.stats = info['stats']
            member.cur_xp = info['xp']

        self.party_index = data['partyIndex']
        self.avg_level = data['avg_level']