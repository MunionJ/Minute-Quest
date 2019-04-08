from MenuSystem.GameMenuStates import GameMenus as menu
from MenuSystem.LandingMenu import *
from MenuSystem.ControlsMenu import *
from MenuSystem.GameMenu import *
from GameEngine.EventManager import *
from GameEngine.DungeonRun import *
from GameEngine.BossFight import BossFight
import pickle

class GameManager:

    def __init__(self):
        self.menuOptions = {}
        self.menuOptions[menu.Main] = LandingMenu()
        self.menuOptions[menu.Loading] = LandingMenu()
        self.menuOptions[menu.NewGame] = GameMenu()
        self.menuOptions[menu.Controls] = ControlsMenu()
        self.menuOptions[menu.PartySelection] = LandingMenu()

        self.game = None
        self.clock = pygame.time.Clock()
        self.running = False
        self.eventmanager = EventManager()   #Incorporate EventManager to handle player input
        self.currentMenuState = None
        pygame.display.set_caption(GAME_NAME)
        self.gameWindow = pygame.display.set_mode(SCREEN_RES)
        self.bg_color = pygame.color.THECOLORS['black']
        self.Partyload = None

    def LoadMenu(self,menuOption):
        currentMenu = self.menuOptions[self.currentMenuState] if self.currentMenuState != None else menu.Main
        newMenu = self.menuOptions[menuOption]
        if currentMenu in self.eventmanager.game_objects['game_menus']:
            self.eventmanager.removeGameMenu(currentMenu)
        self.eventmanager.addGameMenu(newMenu)
        self.currentMenuState = menuOption

    def Launch(self):
        self.LoadMenu(menu.Main)
        self.running = True

    def RunMenuLoop(self):
        while(self.running):
            #Check user input
            self.running = self.eventmanager.process_menu_input()

            #check user selection and determine state
            self.determineState(self.menuOptions[self.currentMenuState])

            #Draw
            if self.running:

                self.gameWindow.fill(self.bg_color)
                self.menuOptions[self.currentMenuState].draw(self.gameWindow)
                pygame.display.update()

    def RunDungeon(self):
        self.game = DungeonRun(self.eventmanager, self.gameWindow)
        self.game.start_game()
        self.game.launch_game()

    def startBossFight(self):
        self.game = BossFight(self.eventmanager, self.gameWindow)
        self.game.start_game()
        self.game.launch_game()

    def Loadsave(self):
        self.Partyload = [self.stats]
        pickle.dump(self.Partyload)

    def determineState(self,currentMenu):
        if currentMenu == None:
            return

        if currentMenu.selectedOption == None:
            return

        selected = currentMenu.getMenuSelection()
        newMenuOption = None

        if self.currentMenuState == menu.Main:
            if selected == "New Game":
                newMenuOption = menu.NewGame
            elif selected == "Load Game":
                newMenuOption = menu.Loading
                self.Loadsave()
                pickle.load(self.Partyload)
            elif selected == "Game Controls":
                newMenuOption = menu.Controls
            elif selected == "Exit":
                self.running = False
        elif self.currentMenuState == menu.NewGame:
            if selected == "Main Menu":
                newMenuOption = menu.Main
            else:
                if selected == "Enter Dungeon":
                    self.RunDungeon()
                elif selected == "Fight The Boss":
                    print("Game Manager, line 85: Selected Boss Fight");
                    self.startBossFight()
                newMenuOption = menu.NewGame
        elif self.currentMenuState == menu.Loading:
            if selected == "New Game":
                newMenuOption = menu.NewGame
            elif selected == "Load Game":
                newMenuOption = menu.Loading
            elif selected == "Game Controls":
                newMenuOption = menu.Controls
            elif selected == "Exit":
                self.running = False
        elif self.currentMenuState == menu.Controls:
            if selected == "Back":
                newMenuOption = menu.Main

        currentMenu.Reset()
        if newMenuOption == None:
            newMenuOption = menu.Main

        self.LoadMenu(newMenuOption)

if __name__ == "__main__":
    gm = GameManager()
    print(gm.currentMenuState)
    gm.loadMenu(menu.Controls)
    print(gm.currentMenuState)



