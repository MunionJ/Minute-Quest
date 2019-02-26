# Test harness for Player class

import pygame
import os
from Enemies import *
from Player import *
from EventManager import *

pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'
bg_color = pygame.color.THECOLORS['black']
window = pygame.display.set_mode(SCREEN_RES)
pygame.display.set_caption("PLAYER TEST HARNESS")
manager = EventManager()
player = Player((window.get_width() // 2, window.get_height() // 2),
                "images/character1")
enemy = Enemy((0, 0), "images/character1")
# the image can be changed back to "images/characters.png" but its the whole sheet
players = pygame.sprite.Group()
players.add(player)

manager.addGameObject(player)
screen_rect = window.get_rect()
clock = pygame.time.Clock()
running = True

while running:
    dt = clock.tick(60) / 1000

    running = manager.process_input(dt)

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    updated_rect = player.rect.clamp(screen_rect)
    player.set_pos(updated_rect)
    window.fill(bg_color)
    for obj in manager.game_objects["game_objects"]:
        obj.draw(window)

    players.draw(window)

    pygame.display.flip()
