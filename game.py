import pygame
from Player import *
from Scene.Dungeon import *
from Scene.Camera import *

class Game:

    def __init__(self, event_mgr, game_window):
        self.window = game_window
        self.manager = event_mgr
        self.running = False
        self.dungeon = Dungeon(4)
        self.player = Player(self.dungeon.playerSpawn, "images/character1")
        self.camera = Camera(self.dungeon)
        self.camera.setCameraPosition(self.player.rect.center)
        self.manager.addGameObject(self.player)
        self.clock = pygame.time.Clock()
        self.bg_color = pygame.color.THECOLORS["black"]
        for room in self.dungeon.rooms:
            for wall in room.walls.sprites():
                self.manager.addGameObject(wall)

    def start_game(self):
        self.running = True

    def launch_game(self):
        while self.running:
            dt = self.clock.tick(60) / 1000

            self.running = self.manager.process_input(dt)

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            updated_rect = self.player.rect.clamp(self.dungeon.rooms[0].bgImageRect)
            # enemy_updated_rect = enemy.rect.clamp(self.dungeon.boundary)
            # enemy.set_pos(enemy_updated_rect)
            self.player.set_pos(updated_rect)
            self.camera.setCameraPosition(self.player.rect.center)
            print(self.player.rect.center, self.player.pos)
            pygame.draw.rect(self.window, (255, 255, 255), self.player.rect, 2)

            self.window.fill(self.bg_color)
            self.camera.draw(self.window)
            # for obj in self.manager.game_objects["game_objects"]:
            #     obj.draw(self.window)

            self.player.draw(self.window)
            # enemy.draw(window)

            pygame.display.flip()
