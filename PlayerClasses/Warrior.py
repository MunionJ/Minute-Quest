import time
from Player import Player


class Warrior(Player):
    """ The playable Warrior character class. This
        character will be the melee damage specialist."""

    def __init__(self, start_pos, img="images/warrior", stats=[3, 1, 1, 20]):
        super().__init__(start_pos, img)
        # CONSTRUCTOR PARAMETERS #
        # stats: a list of initial stats in the order [MELEE, RANGE, MAGIC, MAX_HP]

        self.stats["MELEE"] = stats[0]
        self.stats["RANGE"] = stats[1]
        self.stats["MAGIC"] = stats[2]
        self.stats["CUR_HP"] = stats[3]
        self.stats["MAX_HP"] = stats[3]
        self.base_stats = self.stats
        self.num_rages = 1
        self.rage_timer = 5
        self.rage_active = False

    def use_ability(self):
        """ Method for using class-specific ability."""
        if self.num_rages > 0:
            self.activate_rage()

    def activate_rage(self):
        """ Method for applying the effects of rage."""
        self.rage_active = True
        self.num_rages -= 1
        self.stats["MELEE"] *= 2
        self.stats["CUR_HP"] += self.level * 5

    def deactivate_rage(self):
        """ Method for turning off the effects of rage."""
        self.rage_active = False
        self.stats["MELEE"] = self.base_stats["MELEE"]
        if self.stats["CUR_HP"] > self.stats["MAX_HP"]:
            self.stats["CUR_HP"] = self.stats["MAX_HP"]

    def rage_update(self, dt):
        """ Update the status of the Warrior rage
            ability."""
        self.rage_timer -= dt
        if self.rage_timer <= 0:
            self.deactivate_rage()

    def update(self, keys, dt):
        """ Override for base class update method.
            Has all the same functionality, just added rage
            mechanics for Warrior."""
        super().update(keys, dt)
        if self.rage_active:
            self.rage_update(dt)
