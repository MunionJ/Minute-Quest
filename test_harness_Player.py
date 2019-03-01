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

bottomY = SCREEN_RES[1] - 32
topY = 0
for i in range(int(SCREEN_RES[0]/32)):
    x = i*32
    tileSurf = pygame.Surface((32,32))
    tileSurf.fill(pygame.color.THECOLORS['green'])
    pygame.draw.rect(tileSurf,pygame.color.THECOLORS['black'],pygame.Rect(0,0,32,32),2)
    topRect = pygame.Rect( x, topY, 32, 32)
    bottomRect = pygame.Rect(x, bottomY, 32, 32)
    tiles.add(Tile(tileSurf,topRect))
    tiles.add(Tile(tileSurf, bottomRect))

    if i == 0 or i == int(SCREEN_RES[0]/32) - 1:
        for j in range(1,int(SCREEN_RES[0]/32)-2):
            tiles.add(Tile(tileSurf,pygame.Rect(x, j*32, 32, 32)))

# for i in range(10):
#     x = random.randint(16,SCREEN_RES[0]-16)
#     y = random.randint(16,SCREEN_RES[1]-16)
#     tileSurf = pygame.Surface((32,32))
#     tileSurf.fill(pygame.color.THECOLORS['green'])
#     tileRect = pygame.Rect(0,0,32,32)
#     tileRect.center = (x,y)
#     newTile = Tile(tileSurf,tileRect)
#     collide2 = pygame.sprite.spritecollide(player,tiles,False)
#     while collide2:
#         x = random.randint(16, SCREEN_RES[0] - 16)
#         y = random.randint(16, SCREEN_RES[1] - 16)
#         newTile.rect.center = (x,y)
#         collide2 = pygame.sprite.spritecollide(player, tiles, False)
#     tiles.add(newTile)

manager.addGameObject(player)
#manager.addGameObject(enemy)
screen_rect = window.get_rect()
clock = pygame.time.Clock()
running = True

while running:
    dt = clock.tick(60) / 1000

    #Get Player Input and Apply Physics
    running = manager.process_input(dt)

    #Move Player and Check for Collisions
    player.moveX()
    collisions = pygame.sprite.spritecollide(player, tiles, False)
    if collisions:
        hit = collisions[0]
        player.handleXCollision(hit.rect)

    player.moveY()
    collisions = pygame.sprite.spritecollide(player, tiles, False)
    y_boxes = []
    vertCollisions = False
    if collisions:
        hit = collisions[0]
        player.handleYCollision(hit.rect)
        vertCollisions = True

    # Keep Player on screen
    updated_rect = player.rect.clamp(screen_rect)
    player.set_pos(updated_rect)

    rect = player.rect.copy()

    if not vertCollisions:
        for i in range(PIXEL_DIFFERENCE):
            rect.move_ip(0,1)
            for wall in tiles.sprites():
                if rect.colliderect(wall.rect):
                    player.handleYCollision(wall.rect)
                    vertCollisions = True
                    break
            if vertCollisions:
                break

    if not vertCollisions:
        player.isInAir()

    player.determineState()
    print(player.cur_state)

    #END COLLISION HANDLING

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False


    enemy_updated_rect = enemy.rect.clamp(screen_rect)
    enemy.set_pos(enemy_updated_rect)



    window.fill(bg_color)
    for obj in manager.game_objects["game_objects"]:
        obj.draw(window)

    players.draw(window)
    for tile in tiles.sprites():
        tile.draw(window)

    for box in y_boxes:
        pygame.draw.rect(window,pygame.color.THECOLORS['white'],box,2)

    pygame.display.flip()
