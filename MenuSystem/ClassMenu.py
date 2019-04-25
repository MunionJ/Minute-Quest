import pygame
from GameEngine.Audio import Audio
from config import *
from MenuSystem.Button import Button


class ClassMenu(pygame.sprite.Sprite):

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
            "Warrior",
            "Ranger",
            "Wizard",
            "Paladin",
            "Main Menu"
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
        self.warrior_info = pygame.Surface(self.SCREEN_RES)
        self.ranger_info = pygame.Surface(self.SCREEN_RES)
        self.wizard_info = pygame.Surface(self.SCREEN_RES)
        self.paladin_info = pygame.Surface(self.SCREEN_RES)
        self.blank_bg = pygame.Surface(self.SCREEN_RES)
        self.blank_bg.fill((0, 0, 0))
        self.create_warrior_info()
        self.create_ranger_info()
        self.create_wizard_info()
        self.create_paladin_info()
        self.currentbackground = self.warrior_info

    def Reset(self):
        self.current_index = 0
        self.selectedOption = None
        for button in self.buttons:
            button.deselect()
        self.buttons[self.current_index].select()

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

    def getMenuSelection(self):
        return self.selectedOption

    def setMenuSelection(self):
        self.selectedOption = self.buttonOptions[self.current_index]

    def draw(self, window):
        self.screen.fill(self.bg_color)
        self.screen.blit(self.currentbackground, (0, 0))
        self.screen.blit(self.header, self.headerRect)
        for button in self.buttons:
            button.draw(self.screen)

        window.blit(self.screen, self.rect)

    def create_warrior_info(self):
        xpos = self.screen.get_width() // 2
        ypos = self.screen.get_height() // 2
        self.warrior_info.fill((0, 0, 0))

        text = self.control_font.render("The Warrior is a melee damage powerhouse.",
                                        False,
                                        pygame.color.THECOLORS['white'])
        text2 = self.control_font.render("He can use his Rage ability to temporarily double his",
                                         False,
                                         pygame.color.THECOLORS['white'])
        text3 = self.control_font.render("melee damage, along with exceeding his max HP.",
                                         False,
                                         pygame.color.THECOLORS['white'])
        text4 = self.control_font.render("Starting Stats:",
                                         False,
                                         pygame.color.THECOLORS['white'])
        text5 = self.control_font.render("Max HP: 35",
                                         False,
                                         pygame.color.THECOLORS['white'])
        text6 = self.control_font.render("Melee: 3",
                                         False,
                                         pygame.color.THECOLORS['white'])
        text7 = self.control_font.render("Range: 1",
                                         False,
                                         pygame.color.THECOLORS['white'])
        text8 = self.control_font.render("Magic: 1",
                                         False,
                                         pygame.color.THECOLORS['white'])
        img = pygame.image.load("images/Characters/warrior/right2.png")
        big_img = pygame.transform.scale(img,
                                         (img.get_width() * 8, img.get_height() * 8)
                                         )

        texts = [text, text2, text3, text4, text5, text6, text7, text8]
        for i in range(len(texts)):
            self.warrior_info.blit(texts[i], (xpos, ypos))
            ypos += 40

        self.warrior_info.blit(big_img,
                               (self.screen.get_width() // 1.7, self.screen.get_height() // 3))

    def create_ranger_info(self):
        xpos = self.screen.get_width() // 2
        ypos = self.screen.get_height() // 2
        self.ranger_info.fill((0, 0, 0))

        text = self.control_font.render("The Ranger safely fires arrows from afar.",
                                        False,
                                        pygame.color.THECOLORS['white'])
        text2 = self.control_font.render("He can use his Stealth ability to temporarily avoid",
                                         False,
                                         pygame.color.THECOLORS['white'])
        text3 = self.control_font.render("being detected by enemies.",
                                         False,
                                         pygame.color.THECOLORS['white'])
        text4 = self.control_font.render("Starting Stats:",
                                         False,
                                         pygame.color.THECOLORS['white'])
        text5 = self.control_font.render("Max HP: 22",
                                         False,
                                         pygame.color.THECOLORS['white'])
        text6 = self.control_font.render("Melee: 1",
                                         False,
                                         pygame.color.THECOLORS['white'])
        text7 = self.control_font.render("Range: 3",
                                         False,
                                         pygame.color.THECOLORS['white'])
        text8 = self.control_font.render("Magic: 1",
                                         False,
                                         pygame.color.THECOLORS['white'])
        img = pygame.image.load("images/Characters/ranger/right2.png")
        big_img = pygame.transform.scale(img,
                                         (img.get_width() * 8, img.get_height() * 8))
        texts = [text, text2, text3, text4, text5, text6, text7, text8]
        for i in range(len(texts)):
            self.ranger_info.blit(texts[i], (xpos, ypos))
            ypos += 40
        self.ranger_info.blit(big_img,
                              (self.screen.get_width() // 1.7, self.screen.get_height() // 3)
                              )

    def create_wizard_info(self):
        xpos = self.screen.get_width() // 2
        ypos = self.screen.get_height() // 2
        self.wizard_info.fill((0, 0, 0))

        text = self.control_font.render("The Wizard scorches his foes with fireballs.",
                                        False,
                                        pygame.color.THECOLORS['white'])
        text2 = self.control_font.render("He can use his Time Stop ability to freeze the clock,",
                                         False,
                                         pygame.color.THECOLORS['white'])
        text3 = self.control_font.render("granting some extra time to finish a dungeon.",
                                         False,
                                         pygame.color.THECOLORS['white'])
        text4 = self.control_font.render("Starting Stats:",
                                         False,
                                         pygame.color.THECOLORS['white'])
        text5 = self.control_font.render("Max HP: 17",
                                         False,
                                         pygame.color.THECOLORS['white'])
        text6 = self.control_font.render("Melee: 1",
                                         False,
                                         pygame.color.THECOLORS['white'])
        text7 = self.control_font.render("Range: 1",
                                         False,
                                         pygame.color.THECOLORS['white'])
        text8 = self.control_font.render("Magic: 3",
                                         False,
                                         pygame.color.THECOLORS['white'])
        img = pygame.image.load("images/Characters/wizard/right2.png")
        big_img = pygame.transform.scale(img,
                                         (img.get_width() * 8, img.get_height() * 8))
        texts = [text, text2, text3, text4, text5, text6, text7, text8]
        for i in range(len(texts)):
            self.wizard_info.blit(texts[i], (xpos, ypos))
            ypos += 40
        self.wizard_info.blit(big_img,
                              (self.screen.get_width() // 1.7, self.screen.get_height() // 3)
                              )

    def create_paladin_info(self):
        xpos = self.screen.get_width() // 2
        ypos = self.screen.get_height() // 2
        self.paladin_info.fill((0, 0, 0))

        text = self.control_font.render("The Paladin is a high HP tank.",
                                        False,
                                        pygame.color.THECOLORS['white'])
        text2 = self.control_font.render("He can use his Heal ability to restore HP to the party,",
                                         False,
                                         pygame.color.THECOLORS['white'])
        text3 = self.control_font.render("all while smiting enemies with his axe.",
                                         False,
                                         pygame.color.THECOLORS['white'])
        text4 = self.control_font.render("Starting Stats:",
                                         False,
                                         pygame.color.THECOLORS['white'])
        text5 = self.control_font.render("Max HP: 42",
                                         False,
                                         pygame.color.THECOLORS['white'])
        text6 = self.control_font.render("Melee: 2",
                                         False,
                                         pygame.color.THECOLORS['white'])
        text7 = self.control_font.render("Range: 1",
                                         False,
                                         pygame.color.THECOLORS['white'])
        text8 = self.control_font.render("Magic: 2",
                                         False,
                                         pygame.color.THECOLORS['white'])
        img = pygame.image.load("images/Characters/paladin/right2.png")
        big_img = pygame.transform.scale(img,
                                         (img.get_width() * 8, img.get_height() * 8))
        texts = [text, text2, text3, text4, text5, text6, text7, text8]
        for i in range(len(texts)):
            self.paladin_info.blit(texts[i], (xpos, ypos))
            ypos += 40
        self.paladin_info.blit(big_img,
                               (self.screen.get_width() // 1.7, self.screen.get_height() // 3))

    def update(self, key):
        """Evaluate action based on user keypress"""
        if key == pygame.K_w:
            if self.current_index > 0:
                self.buttons[self.current_index].deselect()
                self.current_index -= 1
                self.buttons[self.current_index].select()

        if key == pygame.K_s:
            if self.current_index < len(self.buttons) - 1:
                self.buttons[self.current_index].deselect()
                self.current_index += 1
                self.buttons[self.current_index].select()

        if self.buttonOptions[self.current_index] == "Warrior":
            self.currentbackground = self.warrior_info
        elif self.buttonOptions[self.current_index] == "Ranger":
            self.currentbackground = self.ranger_info
        elif self.buttonOptions[self.current_index] == "Wizard":
            self.currentbackground = self.wizard_info
        elif self.buttonOptions[self.current_index] == "Paladin":
            self.currentbackground = self.paladin_info
        else:
            self.currentbackground = self.blank_bg

        if key == pygame.K_RETURN:
            if self.buttonOptions[self.current_index] == "Main Menu":
                self.currentbackground = self.warrior_info
                self.setMenuSelection()


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