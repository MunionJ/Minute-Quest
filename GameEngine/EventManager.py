# Names: Jon Munion, Daniel Kratzenberg, Alexander Brown
# ETGG1802-01
# Lab 2: File I/O


import pygame


class EventManager:
    """ This class processes all user input
        events."""
    def __init__(self):
        self.game_objects = {
            'game_objects':[],
            'game_windows':[],
            'game_menus':[],
            'party_objects':[],
            'enemy_objects':[]
        }
        self.joySticks = []

        # check to see if any game pads are connected
        for x in range(0,pygame.joystick.get_count()):
            game_pad = pygame.joystick.Joystick(x)
            game_pad.init()
            print(game_pad.get_name())
            self.joySticks.append(game_pad)

        self.possibleNumberOfPlayers = pygame.joystick.get_count() + 1

    def hasReferenceToGameObject(self,obj):
        return obj in self.game_objects['game_objects']

    def addGameObject(self, obj):
        self.game_objects['game_objects'].append(obj)

    def addParty(self,obj):
        self.game_objects['party_objects'].append(obj)

    def removeGameObject(self,obj):
        self.game_objects['game_objects'].remove(obj)

    def addGameWindow(self, obj):
        self.game_objects['game_windows'].append(obj)

    def removeGameWindow(self, obj):
        self.game_objects['game_windows'].remove(obj)

    def addGameMenu(self, menu):
        self.game_objects['game_menus'].append(menu)

    def removeGameMenu(self,menu):
        self.game_objects['game_menus'].remove(menu)

    def addEnemyObject(self, enemy):
        self.game_objects['enemy_objects'].append(enemy)

    def removeEnemyObject(self,enemy):
        self.game_objects['enemy_objects'].remove(enemy)

    def turnOnDebugMode(self):
        for obj in self.game_objects['game_objects']:
            obj.toggleDebug()

    def process_input(self, dt, updateEnemies, projectiles):
        """ This method processes user input."""
        keys = pygame.key.get_pressed()
        mouseButtons = pygame.mouse.get_pressed()

        if keys[pygame.K_ESCAPE]:
            return False

        temp = None
        # check to see if any game pads are connected
        if len(self.joySticks):
            # 360 pad buttons: 0 = 'A', 1 = 'B', 2 = 'X', 3 = 'Y'
            #                : 4 = 'LB', 5 = 'RB', 6 = 'Back', 7 = 'Start'
            #                : 8 = 'L3', 9 = 'R3'
            #   Axes:
            #               0 - left joystick x axis    (1 = right, -1 = left)
            #               1 - left joystick y axis    (1 = down, -1 = up)
            #               2 - right joystick x axis   (1 = right, -1 = left)
            #               3 - right joystick y axis   (1 = down, -1 = up)
            #               4 - right trigger           (1 is pressed, -1 released) Initialized to 0
            #               5 - left trigger            (1 is pressed, -1 released) Initialized to 0
            #
            #   D-Pad:
            #         game_pad.get_hat(0) Tuple: (horizontal,vertical)
            #          (1,0) Right, (-1,0) Left
            #          (0,1) Up,    (0,-1) Down

            temp = [x for x in keys]
            temp2 = [x for x in mouseButtons]
            for game_pad in self.joySticks:     #Maybe Handle Multiplayer in the future...


                #D_PAD = game_pad.get_hat(0)

                if game_pad.get_axis(0) < -0.25:
                    temp[pygame.K_a] = True
                elif game_pad.get_axis(0) > 0.25:
                    temp[pygame.K_d] = True

                for axis in range(game_pad.get_numaxes()):
                    #print(axis, ": ",game_pad.get_axis(axis))
                    pass

                for hat in range(game_pad.get_numhats()):
                    # PASSING FOR NOW UNTIL WE START ACTUALLY TESTING GAMEPAD
                    pass
                    #print(hat, " ", game_pad.get_hat(hat))

                # check vertical axis on left analog stick
                # if D_PAD[1] > 0:
                #     print(D_PAD[1])
                #     temp[pygame.K_w] = True
                # elif D_PAD[1] < 0:
                #     print(D_PAD[1])
                #     temp[pygame.K_s] = True

                for i in range(game_pad.get_numbuttons()):
                    if(game_pad.get_button(i)):
                        #print(str(i) + " Pressed")
                        pass
                # check status of buttons
                if game_pad.get_button(0):
                    # fill out later
                    temp[pygame.K_SPACE] = True
                if game_pad.get_button(1):
                    pass
                if game_pad.get_button(2):
                    temp[pygame.K_KP_ENTER] = True
                    temp[pygame.K_RETURN] = True
                    temp2[0] = True
                if game_pad.get_button(3):
                    temp2[2] = True
                if game_pad.get_button(5):
                    pass
                if game_pad.get_button(6):
                    pass
                if game_pad.get_button(7):
                    pass
                if game_pad.get_button(8):
                    pass
                if game_pad.get_button(9):
                    pass

                keys = tuple(temp)
                mouseButtons = tuple(temp2)

        for obj in self.game_objects['game_objects']:
            if obj.type == "ENEMY" or obj.type == "PROJECTILE":
                if updateEnemies:
                    obj.update(mouseButtons, keys, dt, projectiles)
            else:
                obj.update(mouseButtons, keys, dt, projectiles)

        for obj in projectiles:
            obj.update(mouseButtons, keys, dt, projectiles)
        #pygame.event.pump()
        return True

    def poll_input(self,dt):
        e = pygame.event.poll()
        evt = None

        # capture D-PAD up and down inputs
        for game_pad in self.joySticks:
            D_PAD = game_pad.get_hat(0)

            if D_PAD[1] > 0:
                evt = pygame.K_w
            elif D_PAD[1] < 0:
                evt = pygame.K_s

        if e.type == pygame.QUIT:
            return False
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                return False
            elif e.key == pygame.K_F1:
                self.turnOnDebugMode()
            else:
                for obj in self.game_objects['party_objects']:
                    obj.update(e.key, dt)
                    
        # if we got a D-PAD input
        elif evt is not None:
            for obj in self.game_objects['party_objects']:
                obj.update(evt, dt)

        return True

    def process_menu_input(self):
        for e in pygame.event.get():

            if e.type == pygame.QUIT:
                return False
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    return False
                elif e.key == pygame.K_F1:
                    self.turnOnDebugMode()
                elif e.key == pygame.K_w or e.key == pygame.K_a or e.key == pygame.K_s or e.key == pygame.K_d or pygame.K_RETURN:
                    for menu in self.game_objects['game_menus']:
                        menu.update(e.key)
            elif e.type == pygame.JOYHATMOTION:
                if e.value[1] > 0:
                    self.updateMenus(pygame.K_w)
                elif e.value[1] < 0:
                    self.updateMenus(pygame.K_s)
            elif e.type == pygame.JOYBUTTONDOWN:
                if e.button == 2:
                    self.updateMenus(pygame.K_RETURN)
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1:
                    print("In EventManager line 217:: CLICK")
                    self.updateMenus(e.pos)

        return True

    def updateMenus(self,key):
        print("In EventManager Line 223:: num_menues = {0}".format(len(self.game_objects['game_menus'])))
        for menu in self.game_objects['game_menus']:
            menu.update(key)

    def cleanup(self):
        """ Method for cleaning out game objects and enemy objects
            after finishing a dungeon run or boss fight.
        """
        self.game_objects['game_objects'].clear()
        self.game_objects['enemy_objects'].clear()
