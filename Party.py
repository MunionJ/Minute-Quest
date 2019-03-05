from Warrior import *
import pygame


class Party:
    """ The Party class will contain a list
        of party members, and handle which party member
        is currently active in gameplay."""
    def __init__(self, start_pos, img_list):
        # CONSTRUCTOR PARAMETERS:
        # mem1, mem2, mem3, mem4: Each one of these is an
        # individual party member

        self.party_members = [Warrior(start_pos, img_list[0], [3, 1, 1, 20]),
                              Warrior(start_pos, img_list[0], [3, 1, 1, 20]),
                              Warrior(start_pos, img_list[0], [3, 1, 1, 20]),
                              Warrior(start_pos, img_list[0], [3, 1, 1, 20])
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
                self.party_index -= 1
                if self.party_index < 0:
                    self.party_index = len(self.party_members) - 1
                self.last_active = 0
            elif key == pygame.K_s:
                self.party_index += 1
                if self.party_index > len(self.party_members) - 1:
                    self.party_index = 0
                self.last_active = 0
            elif key == pygame.K_1:
                self.party_index = 0
                self.last_active = 0
            elif key == pygame.K_2:
                self.party_index = 1
                self.last_active = 0
            elif key == pygame.K_3:
                self.party_index = 2
                self.last_active = 0
            elif key == pygame.K_4:
                self.party_index = 3
                self.last_active = 0
        self.active_member = self.party_members[self.party_index]

    def calc_avg_level(self):
        """ Method for calculating average
            level of the party."""
        pass
