from Player import Player


class Paladin(Player):
    """
    Paladin class: specializes in tanking and heals
    """

    def __init__(self, start_pos, img="images/paladin", stats=[2, 1, 2, 25]):
        super().__init__(start_pos, img)

        self.stats["MELEE"] = stats[0]
        self.stats["RANGE"] = stats[1]
        self.stats["MAGIC"] = stats[2]
        self.stats["CUR_HP"] = stats[3]
        self.stats["MAX_HP"] = stats[3]