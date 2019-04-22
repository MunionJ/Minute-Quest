GAME_NAME = "Minute Quest"

PLAYER_SPAWNS = [79, 13, 356, 212, 216, 181]
PLAYER_EXITS = [96, 55, 360, 223, 199, 182]
ENEMIES_SPAWNS = [69, 6016, 206, 104, 214, 206]
POSSIBLE_KEYS = 93
PUZZLE_RECT1 = [93, 94]
PUZZLE_RECT2 = [205, 206]
PUZZLE_RECT3 = [149, 150]

# Player Variables
PLAYER_GRAV = 35.0
MAX_X_ACC = 55
MAX_X_VEL = 425
PLAYER_ACC = 1000
MAX_Y_VEL = 1000
PLAYER_FRICTION = -20
JUMP_VEC = 325
INVULN_TIMER = 0.75

#Enemy Variables
ENEMY_ACC = 1
ENEMY_MAX_ACC = 2
ENEMY_MAX_VEL = 30
ENEMY_VISION_RANGE = 200

#Projectile Variables
MAX_ACC = 3
MAX_VELOCITY = 400

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

#test

ROOMS = {
    "EnemyRooms": [
        "AB_fight_map1.txt",
        "AB_fight_map2.txt",
        "enemy room.txt",
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
        # "AB_plat_map1.txt", unwinnable
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
