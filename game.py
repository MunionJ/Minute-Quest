import pygame
from Player import *
from Scene.Dungeon import *

class Game:

    def __init__(self):
        self.running = False
        self.dungeon = Dungeon(4)
        self.player = Player()

    def start_game(self):
        pass