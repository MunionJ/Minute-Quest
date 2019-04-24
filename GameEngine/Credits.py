from ParticleEngine.Emitter import Emitter
import time
import pygame

class Credits:

    def __init__(self, event_mgr, game_window):
        self.window = game_window
        x,y,w,h = self.window.get_rect()
        self.SCREEN_RES = (w,h)
        self.manager = event_mgr
        self.running = False
        self.bg_color = pygame.color.THECOLORS["black"]
        self.font_color = pygame.color.THECOLORS['white']
        self.medFont = pygame.font.Font("./fonts/LuckiestGuy-Regular.ttf", 30)
        self.largeFont = pygame.font.Font("./fonts/LuckiestGuy-Regular.ttf", 50)
        self.titleFont = pygame.font.Font("./fonts/LuckiestGuy-Regular.ttf", 100)
        self.group = [
            "daniel_kratzenberg",
            "jon_munion",
            "Alexander_Brown",
            "Mike_Dibble",
        ]
        self.toDisplay = []
        self.margin = 20
        self.midline = self.SCREEN_RES[1]>>1
        self.prepareSequence()
        self.screenTime = 2
        self.step = 5
        self.currentDisplayTime = 0
        self.alphaLevel = 255
        self.maxAlpha = 255
        self.transitioning = True
        self.fadeIn = True
        self.clock = pygame.time.Clock()

    def prepareSequence(self):

        title = self.titleFont.render("Minute Quest", False, self.font_color)
        titleRect = title.get_rect()
        titleRect.center = (self.SCREEN_RES[0]>>1, self.SCREEN_RES[1]>>1)
        self.toDisplay.append([(title,titleRect)] )

        for person in self.group:
            text = None
            with open("./Credits/bios/{0}.txt".format(person), "r") as myfile:
                text = myfile.readlines()
                for i in range(len(text)):
                    text[i] = text[i].strip()

            name = text[0]
            info = text[1]
            about = text[2]

            nameSurf = self.largeFont.render(name,False,self.font_color)
            nameRect = nameSurf.get_rect()
            nameRect.left = self.margin
            nameRect.top = self.margin

            img = pygame.image.load("./Credits/images/{0}.jpg".format(person)).convert()
            if person == "Alexander_Brown":
                img = pygame.transform.rotate(img,90)
            r = img.get_rect()
            ix, iy, iw, ih = r
            ratio = (self.SCREEN_RES[0]/3)/iw
            img = pygame.transform.scale(img, (int(self.SCREEN_RES[0]//3), int(ih*ratio)) )
            r = img.get_rect()
            r.x = self.margin
            r.y = nameRect.bottom + self.margin

            infoSurf = self.medFont.render(info, False, self.font_color)
            infoRect = infoSurf.get_rect()
            infoRect.x = r.right + self.margin
            infoRect.y = r.y

            startX = 0
            startY = 0
            xIndex = startX

            width = self.SCREEN_RES[0] - r.w - 3*self.margin
            height = self.SCREEN_RES[1] - infoRect.h + 10*self.margin

            aboutSurf = pygame.Surface((width,height))
            aboutSurf.fill(self.bg_color)
            aboutRect = aboutSurf.get_rect()
            dash = self.medFont.render("-",False,self.font_color)
            for word in about.split(" "):
                for i in range(len(word)):
                    c = word[i]
                    surf = self.medFont.render(c,False,self.font_color)
                    subR = surf.get_rect()
                    subR.x = xIndex
                    subR.y = startY
                    if subR.right > aboutRect.w:
                        if i != 0 and i != len(word):
                            aboutSurf.blit(dash,subR)
                        xIndex = startX
                        startY += subR.h + 7
                    subR.x = xIndex
                    subR.y = startY
                    xIndex += subR.w + 1
                    aboutSurf.blit(surf,subR)
                xIndex += subR.w + 10

            aboutRect.x = infoRect.x
            aboutRect.y = infoRect.bottom + 5*self.margin

            singleScreen = [(img,r), (nameSurf,nameRect), (infoSurf,infoRect), (aboutSurf, aboutRect)]
            self.toDisplay.append(singleScreen)

    def start_credits(self):
        self.running = True

    def begin_sequence(self):
        while self.running:
            dt = self.clock.tick(60) / 1000
            self.running = self.manager.poll_input(dt)
            if not self.running:
                break

            if self.transitioning:
                self.alphaLevel += -self.step if self.fadeIn else self.step
                if self.alphaLevel <= 0:
                    self.fadeIn = False
                    self.transitioning = False
                if self.alphaLevel >= self.maxAlpha:
                    self.toDisplay.pop(0)
                    self.currentDisplayTime = 0
                    self.alphaLevel = self.maxAlpha
                    self.fadeIn = True
            else:
                self.currentDisplayTime += dt
                if self.currentDisplayTime >= self.screenTime:
                    self.currentDisplayTime = 0
                    self.transitioning = True

            if len(self.toDisplay) == 0:
                break

            self.window.fill(self.bg_color)
            self.draw(self.window, self.toDisplay[0])
            pygame.display.update()

    def draw(self, screen, info):
        for obj in info:
            screen.blit(obj[0],obj[1])

        self.fadeEffect(screen)


    def fadeEffect(self,screen):
            # Fade to Black
            overlay = pygame.Surface(self.SCREEN_RES)
            overlay.fill((0,0,0))
            overlay.set_alpha(self.alphaLevel)
            screen.blit(overlay, (0, 0))


if __name__ == "__main__":
    import os
    from GameEngine.EventManager import *

    running = True
    clock = pygame.time.Clock()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Menu Test")
    screen = pygame.display.set_mode()
    x,y,w,h = screen.get_rect()
    res = (w,h)
    eventManager = EventManager()

    credits = Credits(eventManager,screen)
    credits.start_credits()
    credits.begin_sequence()