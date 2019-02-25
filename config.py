SCREEN_RES = (800,600)
GAME_NAME = "Minute Quest"

#Player Physics
PLAYER_ACC = 0.1
MAX_X_ACC = 0.2
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.8
PLAYER_JUMP_VEL = -15

PLAYER_SPAWNS = [79]
PLAYER_EXITS = [96]
ENEMIES_SPAWNS = [70,6016]

# TEST
PLAYER_GRAV = 0.6

#MAP FILES
ROOMS = {
    "EnemyRooms":[
        #"AB_fight_map1.txt",
        #"AB_fight_map2.txt",
        #"enemy room.txt",
        #"map_enemy_daniel.txt",
        #"MinuteQuestRoom1.txt",
        #"MQ_test_map_battle.txt"
    ],
    "LootRooms":[
        #"AB_loot_map1.txt",
        "map_loot_daniel.txt",
        #"MQ_test_map_loot.txt",
        #"project loot room.txt"
    ],
    "PlatformRooms":[
        #"AB_plat_map1.txt",
        #"map_platformer_daniel.txt",
        "MinuteQuestRoom2.txt",
        #"MQ_test_map_platforming.txt",
        #"project platform room.txt"
    ],
    "PuzzleRooms":[
        "map_puzzle_daniel.txt",
        #"project puzzle room.txt",
        "test.txt"
    ]
}

MAP_SPRITE_SHEET = "../images/ProjectUtumno_full.png"
