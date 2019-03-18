from Player import Player


class Wizard(Player):
    """
    Wizard class, specializes in magic attacks.
    """

    def __init__(self, start_pos, img="images/enemy1", stats=[1, 1, 5, 18]):
        super().__init__(start_pos, img)

        self.stats["MELEE"] = stats[0]
        self.stats["RANGE"] = stats[1]
        self.stats["MAGIC"] = stats[2]
        self.stats["CUR_HP"] = stats[3]
        self.stats["MAX_HP"] = stats[3]
        self.TimeStop = False
        self.delay_timer = 60
        self.TimeStop_timer = 10

    def use_ability(self):
        """Gives the Wizard the power to use his abilities"""
        self.TimeStop = True

    def ability_timer(self, dt):
        if self.TimeStop:
            while self.TimeStop_timer >= 0:
                self.TimeStop_timer -= dt
            while self.delay_timer >=0:
                self.delay_timer -= dt
                self.TimeStop = False
        else:
            pass

