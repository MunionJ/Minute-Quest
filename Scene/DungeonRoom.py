# Names: Jon Munion, Daniel Kratzenberg
# ETGG1802-01
# Lab 2: File I/O

from Scene.MapLoader import loadMap
import pygame
from config import *
from Scene.Tile import *


class DungeonRoom:
    """ This class generates a tile-based map
        from a Flare text file created in the
        Tiled program."""

    def __init__(self, file_name, image_name):
        """ Param: file_name is a string containing the name of
                   the Flare text file with the map data"""
        self.file_name = file_name
        parsed = loadMap(file_name)  # returns map containing header data, tileset data, and layer data
        self.header_data = parsed['header']  # keys: width , height, tilewidth, tileheight, background_color
        self.tile_sets_data = parsed['tileset']  # fname,tile_width,tile_height,gap_x,gap_y
        self.layer_data = parsed['layers']  # array of multidimensional arrays for layer data
        self.currentScene = None  # contains a list of active sprites
        self.sprite_sheet = pygame.image.load(image_name)
        self.tiles_wide = self.sprite_sheet.get_width() // self.header_data['tilewidth']
        self.tiles_high = self.sprite_sheet.get_height() // self.header_data['tileheight']
        self.totalMapWidth = self.header_data['width'] * self.header_data['tilewidth']
        self.totalMapHeight = self.header_data['height'] * self.header_data['tileheight']
        r, g, b, a = tuple(self.header_data['background_color']) if 'background_color' in self.header_data.keys() else (
        0, 0, 0, 255)
        self.bg_color = pygame.Color(r, g, b, a)
        self.boundary = pygame.Rect(0, 0, self.totalMapWidth, self.totalMapHeight)
        tilewidth = self.header_data['tilewidth']
        tileheight = self.header_data['tileheight']
        gap_x = self.tile_sets_data[3]
        gap_y = self.tile_sets_data[4]
        self.bgImage = pygame.Surface((self.totalMapWidth, self.totalMapHeight))
        self.bgImageRect = self.bgImage.get_rect()
        self.exitPoint = None
        self.enemySpawnPoints = []
        self.playerSpawn = None
        self.walls = pygame.sprite.Group()
        self.enemies = []

        for i in range(len(self.layer_data)):
            layer = self.layer_data[i]
            for y in range(len(layer)):
                col = layer[y]
                for x in range(len(col)):
                    tilecode = col[x]
                    source_x = (tilecode) % self.tiles_wide
                    source_y = (tilecode) // self.tiles_wide
                    top_x = (source_x * tilewidth + source_x * gap_x)
                    top_y = source_y * tileheight + source_y * gap_y
                    if tilecode > 1:
                        if i == 0:  # BackGround Layer
                            self.bgImage.blit(
                                self.sprite_sheet,
                                (x * tilewidth, y * tileheight),
                                pygame.Rect(top_x, top_y, tilewidth, tileheight),
                            )
                        elif i == 1:  # Wall Layer
                            tileImage = pygame.Surface((tilewidth, tileheight))
                            tileImage.blit(
                                self.sprite_sheet,
                                (0, 0),
                                pygame.Rect(top_x, top_y, tilewidth, tileheight)
                            )
                            tileImage.set_colorkey(self.bg_color)
                            tile = Tile(
                                tileImage,
                                pygame.Rect(x * tilewidth, y * tileheight, tilewidth, tileheight)
                            )
                            self.walls.add(tile)
                        elif i == 2:  # Spawner Layer
                            if tilecode in ENEMIES_SPAWNS:
                                enemySpawnPoint = pygame.Rect(x * tilewidth, y * tileheight, tilewidth, tileheight)
                                self.enemySpawnPoints.append(enemySpawnPoint)
                            elif tilecode in PLAYER_EXITS:
                                self.exitPoint = pygame.Rect(x * tilewidth, y * tileheight, tilewidth, tileheight)
                            elif tilecode in PLAYER_SPAWNS:
                                self.playerSpawn = pygame.Rect(3 * tilewidth, y * tileheight, tilewidth, tileheight)

    def determineObj(self):
        """
        Determines the objective for a specific room.
        :return: String describing objective
        """
        room_type = self.file_name.split("/")
        room_type = room_type[2:]
        if room_type[0] == "EnemyRooms":
            return "Kill All Enemies!"
        elif room_type[0] == "LootRooms":
            return "Loot!"
        elif room_type[0] == "PlatformRooms":
            return "Platform!"
        elif room_type[0] == "PuzzleRooms":
            type = "Puzzle: "
            if room_type[1] == "map_puzzle_daniel.txt":
                return type + "Combination Key Press"
            elif room_type[1] == "MinuteQuestRoom3.txt":
                return type + "Find the Key to the Exit"
            elif room_type[1] == "project puzzle room.txt":
                return type + "Beat Original Puzzle"

    def draw(self,screen,cameraPos):
        screen.blit(self.bgImage,(int(self.bgImageRect.x - cameraPos[0]), int(self.bgImageRect.y - cameraPos[1])))

        for wall in self.walls:
            # TODO Fix tile draw code
            wall.draw(screen,cameraPos)


        for enemy in self.enemies:
            screen.blit(
                enemy.img,
                (enemy.rect.x - cameraPos[0], enemy.rect.y - cameraPos[1])
            )
