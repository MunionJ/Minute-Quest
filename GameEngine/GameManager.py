from MenuSystem.GameMenuStates import GameMenus as menu
from MenuSystem.LandingMenu import *
from MenuSystem.ControlsMenu import *
from MenuSystem.GameMenu import *
from GameEngine.EventManager import *
from GameEngine.DungeonRun import *
from GameEngine.BossFight import BossFight
from Scene.Loading import Loading
from GameEngine.Audio import Audio
import pickle
from Actors.Party import Party

#stuff
class GameManager:

    def __init__(self):
        pygame.display.set_caption(GAME_NAME)
        self.gameWindow = pygame.display.set_mode()
        x,y,w,h = self.gameWindow.get_rect()
        self.SCREEN_RES = (w,h)

        self.musicManager = Audio()  # handles music playback

        self.loading = Loading(self.SCREEN_RES)    # Loading object
        self.game = None
        self.clock = pygame.time.Clock()
        self.running = False
        self.eventmanager = EventManager()   #Incorporate EventManager to handle player input
        self.currentMenuState = None

        self.menuOptions = {}
        self.menuOptions[menu.Main] = LandingMenu(self.SCREEN_RES)
        self.menuOptions[menu.Loading] = self.menuOptions[menu.Main]
        self.menuOptions[menu.NewGame] = GameMenu(self.SCREEN_RES)
        self.menuOptions[menu.Controls] = ControlsMenu(self.SCREEN_RES)
        self.menuOptions[menu.PartySelection] = self.menuOptions[menu.Main]
        self.bg_color = pygame.color.THECOLORS['black']
        self.Party_Load = None
        self.f_name = "pickle_data.p"

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
#                self.menuOptions[self.currentMenuState].play_sounds()
                pygame.display.update()

    def RunDungeon(self):
        self.loading.draw(self.gameWindow)
        #self.musicManager.play_music(0)
        self.game = DungeonRun(self.eventmanager, self.gameWindow, self.Party_Load)
        self.game.start_game()
        self.game.launch_game()
        self.musicManager.stop_music()
        self.Party_Load = self.game.party_list.partyInfoToPickle()

    def startBossFight(self):
        self.loading.draw(self.gameWindow)
        #self.load_music("PATH TO SONG FOR BOSS")
        #self.musicManager.play_music(0)
        self.game = BossFight(self.eventmanager, self.gameWindow, self.Party_Load)
        self.game.start_game()
        self.game.launch_game()
        self.musicManager.stop_music()
        self.Party_Load = self.game.party_list.partyInfoToPickle()

    def save_game(self):
        if self.Party_Load != None:
            with open(self.f_name, 'wb') as output:  # Overwrites any existing file.
                pickle.dump(self.Party_Load, output, protocol=pickle.HIGHEST_PROTOCOL)

    def Loadsave(self):
        with open(self.f_name, 'rb') as input:
            self.Party_Load = pickle.load(input)

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
                self.Party_Load = None
            elif selected == "Load Game":
                self.Loadsave()
                newMenuOption = menu.NewGame
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
                    self.eventmanager.cleanup()
                elif selected == "Fight The Boss":
                    #print("Game Manager, line 85: Selected Boss Fight");
                    self.startBossFight()
                    self.eventmanager.cleanup()
                elif selected == "Save Game":
                    self.save_game()
                newMenuOption = menu.NewGame

        elif self.currentMenuState == menu.Loading:
            if selected == "New Game":
                newMenuOption = menu.NewGame
            elif selected == "Load Game":
                newMenuOption = menu.Loading
                #TODO:: make method to pull up menu to select game save
                self.Loadsave()
                newMenuOption = menu.NewGame
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



