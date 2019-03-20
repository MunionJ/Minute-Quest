from Actors.Player import Player
import pygame


class Wizard(Player):
    """
    Wizard class, specializes in magic attacks.
    """

    def __init__(self, start_pos, img="images/Characters/wizard", stats=[1, 1, 10, 18]):
        super().__init__(start_pos, img)

        self.class_name = "WIZARD"
        self.stats["MELEE"] = stats[0]
        self.stats["RANGE"] = stats[1]
        self.stats["MAGIC"] = stats[2]
        self.stats["CUR_HP"] = stats[3]
        self.stats["MAX_HP"] = stats[3]
        self.TimeStop = False
        self.NumAbility = 1
        self.DelayTimer = 60
        self.TimeStop_timer = 10

    def use_ability(self, keys):
        """Gives the Wizard the power to use his abilities"""
        if keys[pygame.K_r]:
            if self.NumAbility > 0:
                self.TimeStop = True
            else:
                self.TimeStop = False

    def ability_timer(self, dt):
        """Does the timer for both the ability itself and the cool down timer for using it again"""
        if self.TimeStop:
            while self.TimeStop_timer >= 0:
                self.timer_update(dt)
        else:
            pass

    def timer_update(self, dt):
        """Updates all of the timers"""
        self.TimeStop_timer -= dt
        if self.TimeStop_timer <= 0:
            self.NumAbility -= 1
            self.DelayTimer -= dt
            if self.DelayTimer <= 0:
                self.NumAbility += 1
            self.DelayTimer = 60
        self.TimeStop_timer = 10

    def update(self, *args):
        """Overrides for base class update method.
            Has all the same functionality, just adds the time for Wizard
            mechanics for Wizard. """
        mouseButtons, keys, dt = args
        super().update(*args)
        if self.use_ability(keys):
            self.ability_timer(dt)
