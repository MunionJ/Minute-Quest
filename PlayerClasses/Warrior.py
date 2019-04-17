import pygame
import copy
import random
from Actors.Player import Player
from Weapon import Weapon


class Warrior(Player):
    """ The playable Warrior character class. This
        character will be the melee damage specialist."""

    def __init__(self, start_pos, img="images/Characters/"
                                      "warrior", stats=[3, 1, 1, 35]):
        super().__init__(start_pos, img)
        # CONSTRUCTOR PARAMETERS #
        # stats: a list of initial stats in the order [MELEE, RANGE, MAGIC, MAX_HP]

        self.class_name = "WARRIOR"
        self.stats["MELEE"] = stats[0]
        self.stats["RANGE"] = stats[1]
        self.stats["MAGIC"] = stats[2]
        self.stats["CUR_HP"] = stats[3]
        self.stats["MAX_HP"] = stats[3]

        self.weapons["axe"] = Weapon("images/Weapons/battlehammer.png", (40, 40))
        self.cur_weapon = self.weapons["axe"]
        self.cur_weapon.rect = self.rect.copy()
        self.num_ability_uses = 3
        self.rage_timer = 0     # counts upward to self.max_rage_timer
        self.max_rage_time = 5.25
        self.rage_active = False
        self.weapon_rotated = self.cur_weapon.image

    def use_ability(self, keys, mouseButtons):
        """ Method for using class-specific ability."""
        if keys[pygame.K_r] or mouseButtons[2]:     # mouseButtons[2] = right mouse button
            if self.num_ability_uses > 0:
                self.activate_rage()

    def deal_dmg(self):
        """ Method for dealing damage to an enemy."""
        if self.rage_active:
            return (self.stats["MELEE"] * 2) + self.cur_weapon.atk_pwr
        return self.stats["MELEE"] + self.cur_weapon.atk_pwr

    def activate_rage(self):
        """ Method for applying the effects of rage."""
        if not self.rage_active:
            self.usingAbility = True
            self.rage_active = True
            self.num_ability_uses -= 1
            self.stats["CUR_HP"] += self.stats["MAX_HP"] // 4

    def deactivate_rage(self):
        """ Method for turning off the effects of rage."""
        self.rage_active = False
        self.usingAbility = False
        self.rage_timer = 0
        if self.stats["CUR_HP"] > self.stats["MAX_HP"]:
            self.stats["CUR_HP"] = self.stats["MAX_HP"]

    def rage_update(self, dt):
        """ Update the status of the Warrior rage
            ability."""
        self.rage_timer += dt
        if self.rage_timer >= self.max_rage_time:
            self.deactivate_rage()

    def gain_level(self):
        if self.level < self.max_level:
            super().gain_level()
            hp_gain = random.randint(5, 15)
            self.stats["MAX_HP"] += hp_gain
            self.stats["CUR_HP"] += hp_gain
            self.stats["MELEE"] += random.randint(1, 3)
            self.stats["RANGE"] += random.randint(0, 1)
            self.stats["MAGIC"] += random.randint(0, 1)
            self.max_rage_time += (1 / self.max_level) * 5
            #if self.level == 10 or self.level == 20:
            with open("stat_dump.txt", 'a') as file:
                file.write(self.class_name + '\n')
                file.write("\tLEVEL:" + str(self.level) + '\n')
                for key in self.stats.keys():
                    if key != "CUR_HP":
                        file.write('\t' + key + ":" + str(self.stats[key]) + '\n')
                file.write('\t' + "MAX RAGE TIME: " + str(round(self.max_rage_time, 2)) + " SECONDS\n")

    def update(self, *args):
        """ Override for base class update method.
            Has all the same functionality, just added rage
            mechanics for Warrior."""
        mouseButtons, keys, dt, projectiles = args
        super().update(*args)
        self.use_ability(keys, mouseButtons)
        self.basic_attack(mouseButtons, keys, dt)
        if self.rage_active:
            self.rage_update(dt)
        if self.cur_weapon.active:
            self.cur_weapon.update(dt)

    def draw(self, window, cameraPos):
        super().draw(window,cameraPos)
        # testing player weapon image
