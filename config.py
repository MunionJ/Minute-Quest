SCREEN_RES = (1024, 768)
GAME_NAME = "Minute Quest"

PLAYER_SPAWNS = [79]
PLAYER_EXITS = [96]
ENEMIES_SPAWNS = [70,6016]

# Player Variables
PLAYER_GRAV = 0.6
PLAYER_ACC = 0.5
MAX_X_ACC = 0.2
PLAYER_FRICTION = -0.24

#MAP FILES
ROOMS = {
    "EnemyRooms":[
        #"AB_fight_map1.txt",
        #"AB_fight_map2.txt",
        #"enemy room.txt",
        "map_enemy_daniel.txt",
        "MinuteQuestRoom1.txt",
        # "MQ_test_map_battle.txt"
    ],
    "LootRooms":[
        # "AB_loot_map1.txt",
        "map_loot_daniel.txt",
        # "MQ_test_map_loot.txt",
        # "project loot room.txt"
    ],
    "PlatformRooms":[
        # "AB_plat_map1.txt",
        "map_platformer_daniel.txt",
        "MinuteQuestRoom2.txt",
        # "MQ_test_map_platforming.txt",
        # "project platform room.txt"
    ],
    "PuzzleRooms":[
        "map_puzzle_daniel.txt",
        # "project puzzle room.txt"
    ]
}

MAP_SPRITE_SHEET = "../images/ProjectUtumno_full.png"
