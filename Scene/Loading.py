import pygame
import time


class Loading:
    """ Class for drawing loading/transition screens
        after ending a dungeon run or boss fight.
    """
    def __init__(self, SCREEN_RES):
        self.font = pygame.font.Font("./fonts/LuckiestGuy-Regular.ttf", 50)
        self.transition_timer = 0
        self.max_transition_time = 3
        self.SCREEN_RES = SCREEN_RES

    def draw(self, window, draw_str="LOAD"):
        """ Method for drawing loading/transition screen
            Parameters: window - game screen surface
                        draw_str - a string indicating what needs to be drawn
        """
        draw_str = draw_str.upper()
        window.fill(pygame.color.THECOLORS['black'])
        surf = None
        if draw_str == "LOAD":
            surf = self.font.render("LOADING",
                                    False,
                                    pygame.color.THECOLORS['white']
                                    )

        elif draw_str == "DUNGEON":
            surf = self.font.render("YOU CLEARED THE DUNGEON!",
                                    False,
                                    pygame.color.THECOLORS['white']
                                    )

        elif draw_str == "BOSS":
            surf = self.font.render("YOU DEFEATED THE BOSS!",
                                    False,
                                    pygame.color.THECOLORS['white']
                                    )
        else:
            pass
        rect = surf.get_rect()
        x = self.SCREEN_RES[0] // 2
        y = self.SCREEN_RES[1] // 2
        rect.center = (x, y)
        window.blit(surf, rect)
        pygame.display.flip()
