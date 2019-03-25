import pygame


class Weapon:
    """ The generic Weapon class from which
        more specialized weapons will inherit from."""
    def __init__(self, img, dimensions):
        # CONSTRUCTOR PARAMETERS
        # img: The image used for the weapon sprite
        # dimensions: The width and height of the weapon
        self.atk_pwr = 1
        self.hitbox = dimensions
        self.image = pygame.image.load(img)
        self.frames = {"axe1": self.image}
        for i in self.frames:
            rect = self.frames[i].get_rect()
            width = int(rect.w*(self.hitbox[1]/rect.h))
            height = self.hitbox[1]
            self.frames[i] = pygame.transform.scale(self.frames[i], (width, height))
            self.frames[i] = pygame.transform.flip(self.frames[i], True, False)
            self.frames[i] = self.frames[i].convert_alpha()
        self.image = self.frames["axe1"]
        self.active = False
        self.cur_weapon_timer = 0
        self.max_weapon_timer = 1
        # potential Class attributes:
        # swing speed, ( add more later )

    def update(self, dt):
        """ Method for updating weapon"""
        if self.active:
            if self.cur_weapon_timer < self.max_weapon_timer:
                self.cur_weapon_timer += dt
            else:
                self.cur_weapon_timer = 0
                self.active = False