from Actors.Player import Player


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

    def use_ability(self):
        """ Method for using class-specific ability."""
        if self.num_heals > 0:
            self.activate_heal()

    def activate_heal(self):
        """ Method for applying the effects of heal."""
        self.num_heal -= 1
        self.stats["CUR_HP"] += self.level * 15

    def update(self, *args):
        """ Method called for per frame update"""
        super().update(*args)
        pass
