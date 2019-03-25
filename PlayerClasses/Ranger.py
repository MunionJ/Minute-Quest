from Actors.Player import Player
from Weapon import *


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
        self.weapons["bow"] = Weapon("images/Weapons/w_axe_war_0.png", (40, 40))

    def update(self, *args):
        super().update(*args)
        mouseButtons, keys, dt = args

    def draw(self, window, cameraPos):
        super().draw(window, cameraPos)
        pass