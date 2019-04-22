import pygame
from config import *
from MenuSystem.Button import Button


class ControlsMenu(pygame.sprite.Sprite):

    def __init__(self, SCREEN_RES):
        """Initialize Control Menu"""
        super().__init__()
        self.screen = pygame.Surface(SCREEN_RES)
        self.SCREEN_RES = SCREEN_RES
        self.controller = pygame.image.load("images/controller.png")
        self.controller = pygame.transform.scale(self.controller,
                                                 (int(self.controller.get_width() // 1.3),
                                                  int(self.controller.get_height() // 1.3))
                                                 )
        self.rect = self.screen.get_rect()
        self.font = pygame.font.Font('./fonts/AmaticSC-Regular.ttf', 20)
        self.control_font = pygame.font.Font('./fonts/AmaticSC-Regular.ttf', 40)
        self.gamepad_font = pygame.font.Font('./fonts/AmaticSC-Regular.ttf', 30)
        self.headerFont = pygame.font.Font('./fonts/AmaticSC-Regular.ttf', 75)
        self.headertextColor = pygame.color.THECOLORS['white']
        self.bg_color = pygame.color.THECOLORS['black']
        self.buttonColor = pygame.color.THECOLORS['blue']
        self.buttonTextColor = pygame.color.THECOLORS['white']
        self.buttonSelectColor = pygame.color.THECOLORS['white']
        self.margin = 25

        self.screen.fill(self.bg_color)
        self.header = self.headerFont.render("Controls", False, self.headertextColor)
        self.headerRect = self.header.get_rect()
        self.headerRect.topleft = (self.margin, self.margin)
        self.buttonOptions = [
            "KeyBoard Controls",
            "Gamepad Controls",
            "Back"
        ]
        self.buttons = []
        for option in self.buttonOptions:
            text = self.font.render(option, False, self.buttonTextColor)
            self.buttons.append(Button(text, 0, 0, 300, 50, self.buttonColor, self.buttonSelectColor))

        self.placeButtons()
        self.current_index = 0
        default = self.buttons[self.current_index]
        default.select()
        self.selectedOption = None
        self.keyboardControls = pygame.Surface(self.SCREEN_RES)
        self.gamepadControls = pygame.Surface(self.SCREEN_RES)
        self.createGamePadDisplay()
        self.createKeyBoardDisplay()
        self.currntbackground = self.keyboardControls

    def Reset(self):
        self.current_index = 0
        self.selectedOption = None
        for button in self.buttons:
            button.deselect()
        self.buttons[self.current_index].select()

    def createKeyBoardDisplay(self):
        """Describe Inputs for Users using Keyboard"""
        xpos = 360
        ypos = 100

        self.keyboardControls.fill((0, 0, 0))
        text = self.control_font.render("[A] - Move Left ",
                                        False,
                                        pygame.color.THECOLORS['white'])
        text2 = self.control_font.render("[D] - Move Right ",
                                         False,
                                         pygame.color.THECOLORS['white'])
        text3 = self.control_font.render("[S] - Next character ",
                                         False,
                                         pygame.color.THECOLORS['white'])
        text4 = self.control_font.render("[W] - Previous character ",
                                         False,
                                         pygame.color.THECOLORS['white'])
        text5 = self.control_font.render("[Space] - Jump ",
                                         False,
                                         pygame.color.THECOLORS['white'])
        text6 = self.control_font.render("[Left-Mouse] - Attack",
                                         False,
                                         pygame.color.THECOLORS['white'])
        text7 = self.control_font.render("[Right-Mouse] - Use Ability",
                                         False,
                                         pygame.color.THECOLORS['white'])
        text8 = self.control_font.render("[1] - Select character 1",
                                         False,
                                         pygame.color.THECOLORS['white'])
        text9 = self.control_font.render("[2] - Select character 2",
                                         False,
                                         pygame.color.THECOLORS['white'])
        text10 = self.control_font.render("[3] - Select character 3",
                                          False,
                                          pygame.color.THECOLORS['white'])
        text11 = self.control_font.render("[4] - Select character 4",
                                          False,
                                          pygame.color.THECOLORS['white'])

        texts = [text, text2, text3, text4, text5, text6, text7, text8, text9, text10, text11]
        for i in range(len(texts)):
            self.keyboardControls.blit(texts[i], (xpos, ypos))
            ypos += 40

    def createGamePadDisplay(self):
        """Describe Inputs for Users using Gamepad"""
        self.gamepadControls.fill((0, 0, 0))
        self.gamepadControls.blit(self.controller, (360, 300))
        text = self.gamepad_font.render("Jump",
                                        False,
                                        pygame.color.THECOLORS['white'])
        text2 = self.gamepad_font.render("Attack",
                                         False,
                                         pygame.color.THECOLORS['white'])
        text3 = self.gamepad_font.render("Use Ability",
                                         False,
                                         pygame.color.THECOLORS['white'])
        text4 = self.gamepad_font.render("Movement",
                                         False,
                                         pygame.color.THECOLORS['white'])
        text5 = self.gamepad_font.render("Previous character",
                                         False,
                                         pygame.color.THECOLORS['white'])
        text6 = self.gamepad_font.render("Next character",
                                         False,
                                         pygame.color.THECOLORS['white'])

        # blit jump
        self.gamepadControls.blit(text, (700, 250))
        pygame.draw.line(self.gamepadControls,
                         pygame.color.THECOLORS['white'],
                         (720, 290),
                         (720, 410),
                         2)
        pygame.draw.line(self.gamepadControls,
                         pygame.color.THECOLORS['white'],
                         (720, 410),
                         (670, 410),
                         2)
        # blit attack
        self.gamepadControls.blit(text2, (580, 250))
        pygame.draw.line(self.gamepadControls,
                         pygame.color.THECOLORS['white'],
                         (630, 290),
                         (630, 366),
                         2)

        # blit use ability
        self.gamepadControls.blit(text3, (620, 220))
        pygame.draw.line(self.gamepadControls,
                         pygame.color.THECOLORS['white'],
                         (658, 260),
                         (658, 340),
                         2)

        # blit movement
        self.gamepadControls.blit(text4, (410, 200))
        pygame.draw.line(self.gamepadControls,
                         pygame.color.THECOLORS['white'],
                         (460, 240),
                         (460, 380),
                         2)
        pygame.draw.line(self.gamepadControls,
                         pygame.color.THECOLORS['white'],
                         (440, 380),
                         (480, 380),
                         2)
        pygame.draw.line(self.gamepadControls,
                         pygame.color.THECOLORS['white'],
                         (440, 380),
                         (450, 370),
                         2)
        pygame.draw.line(self.gamepadControls,
                         pygame.color.THECOLORS['white'],
                         (440, 380),
                         (450, 390),
                         2)
        pygame.draw.line(self.gamepadControls,
                         pygame.color.THECOLORS['white'],
                         (480, 380),
                         (470, 370),
                         2)
        pygame.draw.line(self.gamepadControls,
                         pygame.color.THECOLORS['white'],
                         (480, 380),
                         (470, 390),
                         2)

        # blit previous character
        self.gamepadControls.blit(text5, (420, 150))
        pygame.draw.line(self.gamepadControls,
                         pygame.color.THECOLORS['white'],
                         (508, 190),
                         (508, 425),
                         2)

        # blit next character
        self.gamepadControls.blit(text6, (630, 150))
        pygame.draw.line(self.gamepadControls,
                         pygame.color.THECOLORS['white'],
                         (670, 190),
                         (670, 220),
                         2)
        pygame.draw.line(self.gamepadControls,
                         pygame.color.THECOLORS['white'],
                         (670, 220),
                         (550, 220),
                         2)
        pygame.draw.line(self.gamepadControls,
                         pygame.color.THECOLORS['white'],
                         (550, 220),
                         (550, 460),
                         2)
        pygame.draw.line(self.gamepadControls,
                         pygame.color.THECOLORS['white'],
                         (550, 460),
                         (510, 460),
                         2)

    def placeButtons(self):
        """Place buttons on screen"""
        gap_y = self.margin
        totalHeightButton = 0
        for button in self.buttons:
            totalHeightButton += gap_y + button.rect.h

        current_y = self.SCREEN_RES[1] - totalHeightButton
        for button in self.buttons:
            x = self.margin + button.rect.w // 2
            y = current_y
            button.updateLocation(x, y)
            current_y += button.rect.h + 5

    def update(self, key):
        """Evaluate action based on user keypress"""
        if isinstance(key,tuple):
            for i in range(len(self.buttons)):
                button = self.buttons[i]
                if button.rect.collidepoint(key):
                    self.buttons[self.current_index].deselect()
                    self.current_index = i
                    self.buttons[i].select()
                    if i == 2:
                        self.setMenuSelection()
                    break
        else:
            if key == pygame.K_w or key == pygame.K_a:
                if self.current_index > 0:
                    self.buttons[self.current_index].deselect()
                    self.current_index -= 1
                    self.buttons[self.current_index].select()

            if key == pygame.K_s or key == pygame.K_d:
                if self.current_index < len(self.buttons) - 1:
                    self.buttons[self.current_index].deselect()
                    self.current_index += 1
                    self.buttons[self.current_index].select()

        if self.buttonOptions[self.current_index] == "KeyBoard Controls":
            self.currntbackground = self.keyboardControls
        elif self.buttonOptions[self.current_index] == "Gamepad Controls":
            self.currntbackground = self.gamepadControls

        if key == pygame.K_RETURN:
            if self.buttonOptions[self.current_index] == "Back":
                self.setMenuSelection()

    def getMenuSelection(self):
        return self.selectedOption

    def setMenuSelection(self):
        self.selectedOption = self.buttonOptions[self.current_index]

    def draw(self, window):
        self.screen.fill(self.bg_color)
        self.screen.blit(self.currntbackground, (0, 0))
        self.screen.blit(self.header, self.headerRect)
        for button in self.buttons:
            button.draw(self.screen)

        window.blit(self.screen, self.rect)


if __name__ == "__main__":
    import os
    from EventManager import *

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
