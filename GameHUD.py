import pygame


class GameHUD:
    """ This is the HUD class which
        displays party information,
        time remaining, etc."""

    def __init__(self, window):
        self.timer = 60     # seconds
        self.hud_surf = pygame.Surface((100, window.get_height()))

    def draw(self, window, party_list):
        """ Draw pertinent information
            about each party member."""
        x = 10
        y = 20
        bar_width = 75
        bar_height = 15
        self.hud_surf.fill((0, 0, 0))
        for char in party_list.party_members:
            # draw actual hp bar first
            pygame.draw.rect(self.hud_surf,
                             pygame.color.THECOLORS["blue"],
                             (x, y, bar_width, bar_height)
                             )

            # draw outline of hp bar
            pygame.draw.rect(self.hud_surf,
                             pygame.color.THECOLORS["white"],
                             (x, y, bar_width, bar_height),
                             2)

            if char == party_list.active_member:
                pygame.draw.rect(self.hud_surf,
                                 pygame.color.THECOLORS["red"],
                                 (x - 5, y - 20, bar_width + 10, window.get_height() // 4),
                                 1)
            y += window.get_height() // 4
        window.blit(self.hud_surf,
                    (0, 0)
                    )

    def update(self):
        pass