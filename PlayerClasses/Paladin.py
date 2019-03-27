from Actors.Player import Player
from Weapon import Weapon
import pygame

class Paladin(Player):
    """
    Paladin class: specializes in tanking and healing
    """

    def __init__(self, start_pos, img="images/Characters/paladin", stats=[2, 1, 2, 25]):
        super().__init__(start_pos, img)

        self.class_name = "PALADIN"
        self.stats["MELEE"] = stats[0]
        self.stats["RANGE"] = stats[1]
        self.stats["MAGIC"] = stats[2]
        self.stats["CUR_HP"] = stats[3]
        self.stats["MAX_HP"] = stats[3]
        self.weapons["axe"] = Weapon("images/Weapons/waraxe.png", (40, 40))
        self.cur_weapon = self.weapons["axe"]
        self.healPercentage = (.1 + (1/20)*self.level)
        self.numHeals = 1

    def use_ability(self):
        """ Method for using class-specific ability."""
        super().use_ability()

        if self.numHeals > 0:
            self.numHeals -= 1

    def heal_party(self,party):
        for member in party.party_members:
            if member.alive:
                member.healPlayer(int(member.stats["MAX_HP"]*self.healPercentage))

        super().end_ability()

    def update(self, *args):
        """ Method called for per frame update"""
        super().update(*args)
        mouseButtons, keys, dt = args
        if keys[pygame.K_r] or mouseButtons[2]:
            if self.numHeals > 0:
                self.use_ability()
        self.basic_attack(mouseButtons, keys, dt)
        if self.cur_weapon.active:
            self.cur_weapon.update(dt)

    def draw(self, window, cameraPos):
        super().draw(window, cameraPos)
