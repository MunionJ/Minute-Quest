from Player import Player


class Wizard(Player):
    """
    Wizard class, specializes in magic attacks.
    """

    def __init__(self, start_pos, img="images/wizard", stats=[1, 1, 10, 15]):
        super().__init__(start_pos, img)

        self.stats["MELEE"] = stats[0]
        self.stats["RANGE"] = stats[1]
        self.stats["MAGIC"] = stats[2]
        self.stats["CUR_HP"] = stats[3]
        self.stats["MAX_HP"] = stats[3]