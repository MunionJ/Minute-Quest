# Test harness for Player class

import os
from Enemies import *
from Player import *
from EventManager import *
import random
from Scene.Tile import *

pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'
bg_color = pygame.color.THECOLORS['black']
window = pygame.display.set_mode(SCREEN_RES)
pygame.display.set_caption("PLAYER TEST HARNESS")
manager = EventManager()
player = Player((window.get_width() // 2, window.get_height() // 2),
                "images/character1")
enemy = Enemy((0, 0), "images/character1")
players = pygame.sprite.Group()
players.add(player)

tiles = pygame.sprite.Group()
for i in range(10):
    x = random.randint(16,SCREEN_RES[0]-16)
    y = random.randint(16,SCREEN_RES[1]-16)
    tileSurf = pygame.Surface((32,32))
    tileSurf.fill(pygame.color.THECOLORS['green'])
    tileRect = pygame.Rect(0,0,32,32)
    tileRect.center = (x,y)
    newTile = Tile(tileSurf,tileRect)
    collide2 = pygame.sprite.spritecollide(player,tiles,False)
    while collide2:
        x = random.randint(16, SCREEN_RES[0] - 16)
        y = random.randint(16, SCREEN_RES[1] - 16)
        newTile.rect.center = (x,y)
        collide2 = pygame.sprite.spritecollide(player, tiles, False)
    tiles.add(newTile)

manager.addGameObject(player)
manager.addGameObject(enemy)
screen_rect = window.get_rect()
clock = pygame.time.Clock()
running = True


print(len(tiles.sprites()))
while running:
    dt = clock.tick(60) / 1000

    running = manager.process_input(dt)

    player.moveX()
    collisions = pygame.sprite.spritecollide(player, tiles, False)
    for hit in collisions:
        player.handleXCollision(hit.rect)

    player.moveY()
    collisions = pygame.sprite.spritecollide(player, tiles, False)
    for hit in collisions:
        player.handleYCollision(hit.rect)
    else:
        player.isFalling()


    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    updated_rect = player.rect.clamp(screen_rect)
    enemy_updated_rect = enemy.rect.clamp(screen_rect)
    enemy.set_pos(enemy_updated_rect)
    player.set_pos(updated_rect)


    window.fill(bg_color)
    for obj in manager.game_objects["game_objects"]:
        obj.draw(window)

    players.draw(window)
    for tile in tiles.sprites():
        tile.draw(window)

    pygame.display.flip()
