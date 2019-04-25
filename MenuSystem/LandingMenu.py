import pygame
from config import *
from MenuSystem.Button import Button
class LandingMenu(pygame.sprite.Sprite):

    def __init__(self,SCREEN_RES):
        super().__init__()
        self.screen = pygame.Surface(SCREEN_RES)

        self.rect = self.screen.get_rect()
        self.SCREEN_RES = SCREEN_RES
        self.font = pygame.font.Font('./fonts/AmaticSC-Regular.ttf',20)
        self.headerFont = pygame.font.Font('./fonts/AmaticSC-Regular.ttf',100)
        self.headertextColor = pygame.color.THECOLORS['white']
        self.bg_color = pygame.color.THECOLORS['black']
        self.buttonColor = pygame.color.THECOLORS['blue']
        self.buttonTextColor = pygame.color.THECOLORS['white']
        self.buttonSelectColor = pygame.color.THECOLORS['black']
        self.margin = 20
        self.bg_image = pygame.image.load('./images/Frozen Skull tweaked by deevad.png')
        self.bg_image = pygame.transform.scale(self.bg_image,SCREEN_RES)

        self.screen.fill(self.bg_color)
        self.header = self.headerFont.render(GAME_NAME,False,self.headertextColor)
        self.headerRect = self.header.get_rect()
        self.headerRect.midtop = (SCREEN_RES[0]//2, 100)
        self.buttonOptions = [
            "New Game",
            "Load Game",
            "Class Info",
            "Credits",
            "Game Controls",
            "Exit"
        ]
        self.buttons = []
        for option in self.buttonOptions:
            text = self.font.render(option,False,self.buttonTextColor)
            self.buttons.append( Button(text, 0, 0, 300, 50, self.buttonColor,self.buttonSelectColor) )

        self.placeButtons()
        self.current_index = 0
        default = self.buttons[self.current_index]
        default.select()
        self.selectedOption = None

    def Reset(self):
        self.current_index = 0
        self.selectedOption = None
        for button in self.buttons:
            button.deselect()
        self.buttons[self.current_index].select()

    def placeButtons(self):
        gap_y = self.margin
        totalHeightButton = 0
        for button in self.buttons:
            totalHeightButton += gap_y + button.rect.h


        current_y = self.headerRect.bottom + 100
        for button in self.buttons:
            x = (self.SCREEN_RES[0]//2)
            y = current_y
            button.updateLocation(x,y)
            current_y += gap_y + button.rect.h

    def play_music(self):
        pass

    def play_sounds(self):
        pass

    def stop_sounds(self):
        pass

    def update(self,key):

        if isinstance(key,tuple):
            for i in range(len(self.buttons)):
                button = self.buttons[i]
                if button.rect.collidepoint(key):
                    self.buttons[self.current_index].deselect()
                    self.current_index = i
                    self.buttons[i].select()
                    self.setMenuSelection(self.buttonOptions[i])
                    break
        else:
            if key == pygame.K_w or key == pygame.K_a:
                if self.current_index > 0:
                    self.buttons[self.current_index].deselect()
                    self.current_index -= 1
                    self.buttons[self.current_index].select()


            if key == pygame.K_s or key == pygame.K_d:
                if self.current_index < len(self.buttons)-1:
                    self.buttons[self.current_index].deselect()
                    self.current_index += 1
                    self.buttons[self.current_index].select()

            if key == pygame.K_RETURN:
                self.setMenuSelection(self.buttonOptions[self.current_index])

    def getMenuSelection(self):
        self.stop_sounds()
        return self.selectedOption

    def setMenuSelection(self, selected=None):
        self.selectedOption = selected

    def draw(self, window):
        self.screen.fill(self.bg_color)
        self.screen.blit(self.bg_image,(0,0))
        self.screen.blit(self.header,self.headerRect)
        for button in self.buttons:
            button.draw(self.screen)
        window.blit(self.screen,self.rect)

if __name__ == "__main__":
    import os
    from GameEngine.EventManager import EventManager

    running = True
    clock = pygame.time.Clock()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Menu Test")
    screen = pygame.display.set_mode(SCREEN_RES)
    eventManager = EventManager()
    menu = LandingMenu()
    eventManager.addGameMenu(menu)

    while running:

        # UPDATES
        running = eventManager.process_menu_input()

        if not running:
            break

        screen.fill(pygame.color.THECOLORS['black'])
        menu.draw(screen)
        pygame.display.update()


