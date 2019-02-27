
from Player import Player


class Warrior(Player):
    """ The playable Warrior character class. This
        character will be the melee damage specialist."""

    def __init__(self, start_pos, img):
        super().__init__(start_pos, img)
