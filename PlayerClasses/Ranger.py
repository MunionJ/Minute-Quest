from Actors.Player import Player
from Projectile import Projectile
from Weapon import *
import config


class Ranger(Player):
    """
    Ranger class, specializes in ranged attacks.
    """

    def __init__(self, start_pos, img="images/Characters/ranger", stats=[1, 3, 1, 15]):
        super().__init__(start_pos, img)

        self.class_name = "RANGER"
        self.stats["MELEE"] = stats[0]
        self.stats["RANGE"] = stats[1]
        self.stats["MAGIC"] = stats[2]
        self.stats["CUR_HP"] = stats[3]
        self.stats["MAX_HP"] = stats[3]
        self.weapons["bow"] = Weapon("images/Weapons/enchantedbow.png", (32, 32))
        self.cur_weapon = self.weapons["bow"]
        self.cur_weapon.rect = self.rect.copy()
        self.cur_weapon.rect.x = self.cur_weapon.rect.x + 15
        self.num_ability_uses = 2
        self.base_attack_cooldown = 0.5
        self.last_base_attack = 0

    def basic_attack(self, mbuttons, keys, dt, projectiles):
        if mbuttons[0]:
            if self.last_base_attack <= 0 and self.camera_offset is not None:
                super().basic_attack(mbuttons, keys, dt)
                mosPos = pygame.mouse.get_pos()
                tX = mosPos[0] + self.camera_offset[0]
                tY = mosPos[1] + self.camera_offset[1]
                p = Projectile('images/Weapons/arrow.png', 32, 32, self.rect.midtop, (tX, tY))
                projectiles.append(p)
                self.last_base_attack = self.base_attack_cooldown
        self.last_base_attack -= dt


    def use_ability(self, keys, mouseButtons):
        """ Method for using class-specific ability."""
        if keys[pygame.K_r] or mouseButtons[2] and self.num_ability_uses > 0:
            self.activate_stealth()

    def activate_stealth(self):
        super().use_ability()
        self.invuln_timer = self.abilityCoolDown
        if self.is_seen is True:
            self.is_seen = False

    def deactivate_stealth(self):
        self.invuln_timer = 0
        super().end_ability()

    def stealth_update(self, dt):
        self.currentAbilityTimer -= dt
        if self.currentAbilityTimer <= 0:
            self.deactivate_stealth()
            self.currentAbilityTimer = self.abilityCoolDown
            self.num_ability_uses -= 1
        elif self.usingAbility is True and self.cur_weapon.active:
            self.deactivate_stealth()
            self.currentAbilityTimer = self.abilityCoolDown
            self.num_ability_uses -= 1

    def update(self, *args):
        super().update(*args)
        mouseButtons, keys, dt, projectiles = args
        self.use_ability(keys, mouseButtons)
        self.basic_attack(mouseButtons, keys, dt, projectiles)
        if self.usingAbility is True:
            self.stealth_update(dt)
        if self.cur_weapon.active:
            self.cur_weapon.update(dt)

    def deal_dmg(self):
        return self.stats["RANGE"] + self.cur_weapon.atk_pwr

    def draw(self, window, cameraPos):
        super().draw(window, cameraPos)
