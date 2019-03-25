from Actors.Player import Player
from Weapon import Weapon
import pygame

class Paladin(Player):
    """
    Paladin class: specializes in tanking
    """

    def __init__(self, start_pos, img="images/Characters/paladin", stats=[2, 1, 2, 25]):
        super().__init__(start_pos, img)

        self.class_name = "PALADIN"
        self.stats["MELEE"] = stats[0]
        self.stats["RANGE"] = stats[1]
        self.stats["MAGIC"] = stats[2]
        self.stats["CUR_HP"] = stats[3]
        self.stats["MAX_HP"] = stats[3]
        self.num_heals = 1 + int(self.level//3)
        self.weapons["axe"] = Weapon("images/Weapons/w_axe_war_0.png", (40, 40))
        self.cur_weapon = self.weapons["axe"]

    def use_ability(self, keys, mouseButtons):
        """ Method for using class-specific ability."""
        if keys[pygame.K_r] or mouseButtons[2]:
            if self.num_heals > 0:
                self.activate_heal()

    def activate_heal(self):
        """ Method for applying the effects of heal."""
        self.num_heal -= 1
        self.stats["CUR_HP"] += self.level * 15

    def update(self, *args):
        """ Method called for per frame update"""
        mouseButtons, keys, dt = args
        super().update(*args)
        self.basic_attack(mouseButtons, keys, dt)
        if self.weapon_active:
            self.weapon_update(dt)
        pass

    def draw(self, window, cameraPos):
        super().draw(window, cameraPos)
        # testing player weapon image
        if self.cur_weapon is not None:
            if self.weapon_active:
                window.blit(self.cur_weapon.image,
                            (self.rect.x - cameraPos[0] + 15, self.rect.y - cameraPos[1])
                            )