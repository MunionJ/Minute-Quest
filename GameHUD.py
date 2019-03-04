import pygame


class GameHUD:
    """ This is the HUD class which
        displays party information,
        time remaining, etc."""

    def __init__(self, window):
        self.timer = 60     # seconds
        self.hud_surf = pygame.Surface((100, window.get_height()))
        self.font = pygame.font.SysFont("Times New Roman",
                                        30)

    def draw(self, window, party_list):
        """ Draw pertinent information
            about each party member, as well
            as the remaining time."""
        x = 10
        y = 20
        bar_width = 75
        bar_height = 15
        self.hud_surf.fill((0, 0, 0))
        for char in party_list.party_members:
            if char == party_list.active_member:
                pygame.draw.rect(self.hud_surf,
                                 pygame.color.THECOLORS["red"],
                                 (x - 5, y - 20, bar_width + 10, window.get_height() // 4),
                                 1)
                # draw actual hp bar first
                pygame.draw.rect(self.hud_surf,
                                 pygame.color.THECOLORS["blue"],
                                 (x, y, bar_width, bar_height)
                                 )
            else:
                # gray out hp bar for inactive members
                pygame.draw.rect(self.hud_surf,
                                 pygame.color.THECOLORS["gray"],
                                 (x, y, bar_width, bar_height)
                                 )
            # draw outline of hp bar
            pygame.draw.rect(self.hud_surf,
                             pygame.color.THECOLORS["white"],
                             (x, y, bar_width, bar_height),
                             2)
            self.hud_surf.blit(char.rframes[1],
                               (x, y + 20)
                               )
            y += window.get_height() // 4
        # blit hud surface onto main game window
        window.blit(self.hud_surf,
                    (0, 0)
                    )
        # blit timer onto main game window
        font_surf = self.font.render(str(round(self.timer, 1)),
                                     False,
                                     (pygame.color.THECOLORS["white"])
                                     )
        window.blit(font_surf,
                    (window.get_width() // 2, 30)
                    )

    def update(self, keys, dt):
        """ Updates remaining time for given playable
            segment ( dungeon, town, etc. )"""
        self.timer -= dt
