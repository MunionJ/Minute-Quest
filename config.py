SCREEN_RES = (800, 600)
GAME_NAME = "Minute Quest"

PLAYER_SPAWNS = [79, 13, 356, 212]
PLAYER_EXITS = [96, 55, 360, 216]
ENEMIES_SPAWNS = [70, 6016]

# Player Variables
PLAYER_GRAV = 1.2
PLAYER_ACC = 9
MAX_X_ACC = 5
PLAYER_FRICTION = -0.24
JUMP_VEC = 1.5

WALLS_ONE = ["MQ_test_map_battle", "AB_fight_map1", "AB_fight_map2", "enemy room", "MinuteQuestRoom1", "AB_loot_map1",
             "MQ_test_map_loot", "project loot room", "AB_plat_map1.txt", "MQ_test_map_platforming",
             "project platform room", "project puzzle room"]
UTUMNO = ["map_enemy_daniel", "map_platformer_daniel", "MinuteQuestRoom2", "map_puzzle_daniel", "map_loot_daniel"]

# MAP FILES
ROOMS = {
    "EnemyRooms": [
        # "AB_fight_map1.txt",
        # "AB_fight_map2.txt",
        "enemy room.txt",
        "map_enemy_daniel.txt",
        # "MinuteQuestRoom1.txt",
        # "MQ_test_map_battle.txt"
    ],
    "LootRooms": [
        # "AB_loot_map1.txt",
        "map_loot_daniel.txt",
        # "MQ_test_map_loot.txt",
        "project loot room.txt"
    ],
    "PlatformRooms": [
        # "AB_plat_map1.txt",
        "map_platformer_daniel.txt",
        "MinuteQuestRoom2.txt",
        # "MQ_test_map_platforming.txt",
        "project platform room.txt"
    ],
    "PuzzleRooms": [
        # "map_puzzle_daniel.txt",
        # "project puzzle room.txt"
    ]
}
