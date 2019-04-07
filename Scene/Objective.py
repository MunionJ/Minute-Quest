import pygame
import random

#TODO::Needs Integrated into Dungeon Room

class Objective:

    def __init__(self,file_name):
        room_type = file_name.split("/")
        self.announcement = None
        self.completed = False
        splitstring = room_type[2:]
        self.room_type = splitstring[0]
        self.room_name = splitstring[1]
        if self.room_type == "EnemyRooms":
            self.announcement = "Kill All Enemies!"
        elif self.room_type == "LootRooms":
            self.announcement = "Loot!"
        elif self.room_type == "PlatformRooms":
            self.announcement = "Platform!"
        elif self.room_type == "PuzzleRooms":
            type = "Puzzle: "
            if self.room_name == "map_puzzle_daniel.txt":
                self.announcement = type + "Combination Key Press"
                validInputs = [("W",pygame.K_w),("S",pygame.K_s),("JUMP",pygame.K_SPACE),("ATTACK",(1,0,0))]
                self.targetInputs = []
                self.playerInputss = []
                for i in range(5):
                    self.targetInputs.append(random.choice(validInputs))

            elif self.room_name == "MinuteQuestRoom3.txt":
                self.announcement = type + "Find the Key to the Exit"
            elif self.room_name == "project puzzle room.txt":
                self.announcement = type + "Beat Original Puzzle"
        elif self.room_type == "boss rooms":
            self.announcement = ""
        else:
            self.completed = True

    def isComplete(self):
        return self.completed

    def evaluateObjective(self,player,playerBoundary,currentRoom,enemyList):
        #if self.room_type ==

        complete = False
        if self.room_type == "EnemyRooms":
            if(len(enemyList) == 0):
                complete = True
        elif self.room_type == "LootRooms":
            if not self.completed:
                complete = True
        elif self.room_type == "PlatformRooms":
            if player.rect.colliderect(currentRoom.exitPoint):
                complete = True
        elif self.room_type == "PuzzleRooms":
            type = "Puzzle: "
            if self.room_name == "map_puzzle_daniel.txt":
                events = pygame.event.get()
                for e in events:
                    if e.type == pygame.KEYDOWN:
                        if self.targetInputs[0][1] == e.key:
                            self.playerInputs.append(e.key)
                        else:
                            self.playerInputs = []
                    elif e.type == pygame.MOUSEBUTTONDOWN:
                        if self.targetInputs[0][1] == e.button:
                            self.playerInputs.append(e.button)
                        else:
                            self.playerInputs = []

                if len(self.targetInputs) == len(self.playerInputs):
                    complete = True

            elif self.room_name == "MinuteQuestRoom3.txt":
                #add in find key logic
                pass
            elif self.room_name == "project puzzle room.txt":
                #add in puzzle logic
                pass
        elif self.room_type == "boss rooms":
            if len(enemyList) == 0:
                complete = True

        if complete and not self.completed:
            self.completed = True
            playerBoundary = playerBoundary.union(currentRoom.bgImageRect)
