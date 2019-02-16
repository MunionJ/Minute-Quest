import pygame
import os
from GameManager import *

# Initialization
pygame.init()
pygame.joystick.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.display.set_caption("Test Map")

manager = GameManager()
manager.Launch()
manager.RunMenuLoop()

pygame.quit()
exit()