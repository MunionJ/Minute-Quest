import pygame
import os
from GameEngine.GameManager import *

# Initialization
pygame.init()
pygame.joystick.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.display.set_caption("Minute Quest")

manager = GameManager()
manager.Launch()
manager.RunMenuLoop()

pygame.quit()
exit()
