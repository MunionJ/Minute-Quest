import pygame
from config import *
from MenuSystem.Button import Button


class ControlsMenu(pygame.sprite.Sprite):

    def __init__(self):
        """Initialize Control Menu"""
        super().__init__()
        self.screen = pygame.Surface(SCREEN_RES)
        self.controller = pygame.image.load("images/controller.png")
        self.rect = self.screen.get_rect()
        self.font = pygame.font.Font('./fonts/AmaticSC-Regular.ttf', 20)
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
        self.keyboardControls = pygame.Surface(SCREEN_RES)
        self.gamepadControls = pygame.Surface(SCREEN_RES)
        self.createGamePadDisplay()
        self.createKeyBoardDisplay()

    def Reset(self):
        self.current_index = 0
        self.selectedOption = None
        for button in self.buttons:
            button.deselect()
        self.buttons[self.current_index].select()

    def createKeyBoardDisplay(self):
        """Describe Inputs for Users using Keyboard"""

        pygame.Surface.fill(self.keyboardControls,(0, 0, 0))
        text = pygame.font.Font.render(self.font, "The wasd keys move the character w is jump b is attack and v is crotch ", 12, (0,0,0))
        pygame.Surface.blit(self.keyboardControls,text, (0, 0))
        pass

    def createGamePadDisplay(self):
        """Describe Inputs for Users using Gamepad"""
        controller: object = self.controller
        pygame.Surface.fill(self.gamepadControls,(0, 0, 0))
        pygame.Surface.blit(self.gamepadControls, controller, (300, 200))
        text = pygame.font.Font.render(self.font,
            "The joystick moves along with the d pad up is jump the a button is attack and the b button is crotch", 12, (0,0,0))
        pygame.Surface.blit(self.gamepadControls, text, (0, 0))
        pass

    def placeButtons(self):
        """Place buttons on screen"""
        gap_y = self.margin
        totalHeightButton = 0
        for button in self.buttons:
            totalHeightButton += gap_y + button.rect.h

        current_y = SCREEN_RES[1] - totalHeightButton - self.margin
        for button in self.buttons:
            x = self.margin + button.rect.w // 2
            y = current_y
            button.updateLocation(x, y)
            current_y += button.rect.h + 5

    def update(self, key):
        """Evaluate action based on user keypress"""
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
            pass
        elif self.buttonOptions[self.current_index] == "Gamepad Controls":
            pass

        if key == pygame.K_RETURN:
            if self.buttonOptions[self.current_index] == "Back":
                self.setMenuSelection()

    def getMenuSelection(self):
        return self.selectedOption

    def setMenuSelection(self):
        self.selectedOption = self.buttonOptions[self.current_index]

    def draw(self, window):
        self.screen.fill(self.bg_color)
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
