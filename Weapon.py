

class Weapon:
    """ The generic Weapon class from which
        more specialized weapons will inherit from."""
    def __init__(self, img):
        # CONSTRUCTOR PARAMETERS
        # img: The image used for the weapon sprite
        self.atk_pwr = None
        # potential Class attributes:
        # swing speed, ( add more later )