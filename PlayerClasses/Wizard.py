from Actors.Player import Player
import pygame
import random
from Weapon import Weapon
from Projectiles.FireBall import FireBall


class Wizard(Player):
    """
    Wizard class, specializes in magic attacks.
    """

    def __init__(self, start_pos, img="images/Characters/wizard", stats=[1, 1, 3, 17]):
        super().__init__(start_pos, img)

        self.class_name = "WIZARD"
        self.stats["MELEE"] = stats[0]
        self.stats["RANGE"] = stats[1]
        self.stats["MAGIC"] = stats[2]
        self.stats["CUR_HP"] = stats[3]
        self.stats["MAX_HP"] = stats[3]
        self.weapons["staff"] = Weapon("images/Weapons/earthstaff.png", (40, 40))
        self.cur_weapon = self.weapons["staff"]
        self.cur_weapon.rect = self.rect.copy()
        self.num_ability_uses = 1
        self.DelayTimer = 60
        self.TimeStop_timer = 5
        self.useAbility = False
        self.weapon_rotated = self.cur_weapon.image
        self.base_attack_cooldown = 0.5
        self.last_base_attack = 0

    def basic_attack(self, mbuttons, keys, dt, projectiles):
        if mbuttons[0]:
            if self.last_base_attack <= 0 and self.camera_offset is not None:
                super().basic_attack(mbuttons, keys, dt)
                mosPos = pygame.mouse.get_pos()
                tX = mosPos[0] + self.camera_offset[0]
                tY = mosPos[1] + self.camera_offset[1]
                p = FireBall('images/Weapons/fireball.png', 40, 20, self.rect.center, (tX, tY), self.stats["MAGIC"])
                projectiles.append(p)
                self.last_base_attack = self.base_attack_cooldown
        self.last_base_attack -= dt

    def use_ability(self):
        """Gives the Wizard the power to use his abilities"""
        super().use_ability()

    def deal_dmg(self):
        return self.stats["MAGIC"]

    def gain_level(self):
        if self.level < self.max_level:
            super().gain_level()
            hp_gain = random.randint(3, 9)
            self.stats["MAX_HP"] += hp_gain
            self.stats["CUR_HP"] += hp_gain
            self.stats["MELEE"] += random.randint(0, 1)
            self.stats["RANGE"] += random.randint(0, 1)
            self.stats["MAGIC"] += random.randint(2, 3)
            self.TimeStop_timer += (1 / self.max_level) * 5
            if self.level == 10 or self.level == 20:
                with open("stat_dump.txt", 'a') as file:
                    file.write(self.class_name + '\n')
                    file.write("\tLEVEL:" + str(self.level) + '\n')
                    for key in self.stats.keys():
                        if key != "CUR_HP":
                            file.write('\t' + key + ":" + str(self.stats[key]) + '\n')

    def ability_timer(self, dt):
        """Does the timer for both the ability itself and the cool down timer for using it again"""
        if self.TimeStop:
            while self.TimeStop_timer >= 0:
                self.timer_update(dt)
        else:
            pass

    def timer_update(self, dt):
        """Updates all of the timers"""
        if self.usingAbility:
            self.TimeStop_timer -= dt
            if self.TimeStop_timer <= 0:
                self.DelayTimer -= dt
                super().end_ability()

    def update(self, *args):
        """Overrides for base class update method.
            Has all the same functionality, just adds the time for Wizard
            mechanics for Wizard. """
        mouseButtons, keys, dt, projectiles = args
        super().update(*args)
        if keys[pygame.K_r] or mouseButtons[2]:
            if self.num_ability_uses > 0:
                self.use_ability()
                self.num_ability_uses -= 1
        self.timer_update(dt)
        self.basic_attack(mouseButtons, keys, dt, projectiles)
        if self.cur_weapon.active:
            self.cur_weapon.update(dt)

    def draw(self, window, cameraPos):
        super().draw(window, cameraPos)

