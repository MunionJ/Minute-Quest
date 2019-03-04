SCREEN_RES = (800, 600)
GAME_NAME = "Minute Quest"

PLAYER_SPAWNS = [79, 13, 356, 212, 216]
PLAYER_EXITS = [96, 55, 360, 223, 199]
ENEMIES_SPAWNS = [70, 6016, 206, 215]
POSSIBLE_KEYS = [94]

# Player Variables
PLAYER_GRAV = 1.2
PLAYER_ACC = 2
MAX_X_ACC = 2
PLAYER_FRICTION = -0.24
JUMP_VEC = 1.5

#Maximum offset of pixels between an actor on a surface to determine if a player is on a surface
PIXEL_DIFFERENCE = 2

WALLS_ONE = [
    "MQ_test_map_battle", "AB_fight_map1", "AB_fight_map2",
     "enemy room", "AB_loot_map1",
     "MQ_test_map_loot", "project loot room", "AB_plat_map1.txt",
     "MQ_test_map_platforming", "project platform room", "project puzzle room"
 ]

UTUMNO = [
    "map_enemy_daniel", "map_platformer_daniel", "MinuteQuestRoom2",
    "map_puzzle_daniel", "map_loot_daniel", "MinuteQuestRoom3", "MinuteQuestRoom1"
]

# MAP FILES
ROOMS = {
    "EnemyRooms": [
        "AB_fight_map1.txt",
        "AB_fight_map2.txt",
        "enemy room.txt",        #TODO Fix holes
        "map_enemy_daniel.txt",
        "MinuteQuestRoom1.txt",
        "MQ_test_map_battle.txt"
    ],
    "LootRooms": [
        "AB_loot_map1.txt",
        "map_loot_daniel.txt",
        "MQ_test_map_loot.txt",
        "project loot room.txt"
    ],
    "PlatformRooms": [
        "AB_plat_map1.txt",
        "map_platformer_daniel.txt",
        "MinuteQuestRoom2.txt",
        "MQ_test_map_platforming.txt",
        "project platform room.txt"
    ],
    "PuzzleRooms": [
        "map_puzzle_daniel.txt",
        "project puzzle room.txt",
        "MinuteQuestRoom3.txt"
    ]
}
