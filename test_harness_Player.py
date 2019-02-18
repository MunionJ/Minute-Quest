# Test harness for Player class

import pygame
import os
from Player import *
from EventManager import *

pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'
screen_size = (1024, 768)
bg_color = pygame.color.THECOLORS['black']
window = pygame.display.set_mode(screen_size)
pygame.display.set_caption("PLAYER TEST HARNESS")
manager = EventManager()
player = Player((window.get_width() // 2, window.get_height() // 2),
                "images/characters.png")

manager.addGameObject(player)
screen_rect = window.get_rect()
clock = pygame.time.Clock()
running = True

while running:
    dt = clock.tick(60)
    running = manager.process_input(dt)

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    screen_rect.clamp_ip(player.rect)
    window.fill(bg_color)
    for obj in manager.game_objects["game_objects"]:
        obj.draw(window)

    pygame.display.flip()
