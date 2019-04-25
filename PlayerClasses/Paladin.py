from Actors.Player import Player
from Weapon import Weapon
import pygame
import random


class Paladin(Player):
    """
    Paladin class: specializes in tanking and healing
    """

    def __init__(self, start_pos, img="images/Characters/paladin", stats=[2, 1, 2, 42]):
        super().__init__(start_pos, img)

        self.class_name = "PALADIN"
        self.healPercentage = (.1 + (1 / self.max_level) * self.level)
        self.stats["MELEE"] = stats[0]
        self.stats["RANGE"] = stats[1]
        self.stats["MAGIC"] = stats[2]
        self.stats["CUR_HP"] = stats[3]
        self.stats["MAX_HP"] = stats[3]
        self.stats["ABILITY"] = self.healPercentage
        self.weapons["axe"] = Weapon("images/Weapons/waraxe.png", (40, 40))
        self.cur_weapon = self.weapons["axe"]
        self.cur_weapon.rect = self.rect.copy()
        self.cur_weapon.rect.x = self.cur_weapon.rect.x + 15
        self.num_ability_uses = 1
        self.weapon_rotated = self.cur_weapon.image

    def use_ability(self):
        """ Method for using class-specific ability."""
        super().use_ability()

        if self.num_ability_uses > 0:
            self.num_ability_uses -= 1

    def deal_dmg(self):
        return self.stats["MELEE"] + (self.stats["MAGIC"] // 2) + self.cur_weapon.atk_pwr

    def gain_level(self):
        if self.level < self.max_level:
            super().gain_level()
            hp_gain = random.randint(6, 18)
            self.stats["MAX_HP"] += hp_gain
            self.stats["CUR_HP"] += hp_gain
            self.stats["MELEE"] += random.randint(1, 2)
            self.stats["RANGE"] += random.randint(0, 1)
            self.stats["MAGIC"] += random.randint(1, 2)
            self.stats["ABILITY"] += (1 / self.max_level ** 1.333)
            if self.level == 10 or self.level == 20:
                with open("stat_dump.txt", 'a') as file:
                    file.write(self.class_name + '\n')
                    file.write("\tLEVEL:" + str(self.level) + '\n')
                    for key in self.stats.keys():
                        if key != "CUR_HP":
                            if key == "ABILITY":
                                file.write('\t' + key + ":" + str(round(self.stats[key], 2) * 100) + '%' + '\n')
                            else:
                                file.write('\t' + key + ":" + str(self.stats[key]) + '\n')

    def heal_party(self,party):
        for member in party.party_members:
            if member.alive and member.stats['CUR_HP'] < member.stats['MAX_HP']:
                member.healPlayer(int(member.stats["MAX_HP"]*self.stats["ABILITY"]))

        super().end_ability()

    def update(self, *args):
        """ Method called for per frame update"""
        super().update(*args)
        mouseButtons, keys, dt, projectiles = args
        if keys[pygame.K_r] or mouseButtons[2]:
            if self.num_ability_uses > 0:
                self.use_ability()
        self.basic_attack(mouseButtons, keys, dt)
        if self.cur_weapon.active:
            self.cur_weapon.update(dt)

    def draw(self, window, cameraPos):
        super().draw(window, cameraPos)
