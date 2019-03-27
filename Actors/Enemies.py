from Actors.Actor import *
import time

class Enemy(Actor):
    """Basic enemy class that creates the properties/methods shared across all enemies."""

    def __init__(self, spawn_point, img):
        super().__init__(spawn_point)
        self.enemyHeight = 48
        self.level = 1
        self.alive = True
        self.t_anim = time.time() + 0.125  # timer used for animations
        self.anim = 0  # which frame of animations are active.
        self.rframes = [pygame.image.load(img + "/right1.png"),
                        pygame.image.load(img + "/right2.png"),
                        pygame.image.load(img + "/right3.png"),
                        pygame.image.load(img + "/right2.png")]
        self.frames = {"right": pygame.image.load(img + "/right1.png"),
                       "rjump": pygame.image.load(img + "/jump1.png"), }
        # dictionary of frames.  the values will be updating to make animations
        for i in self.frames:
            rect = self.frames[i].get_rect()
            width = int(rect.w * (self.enemyHeight / rect.h))
            height = self.enemyHeight
            self.frames[i] = pygame.transform.scale(self.frames[i], (width, height))
            self.frames[i] = self.frames[i].convert_alpha()
        for i in range(len(self.rframes)):
            rect = self.rframes[i].get_rect()
            width = int(rect.w * (self.enemyHeight / rect.h))
            height = self.enemyHeight
            self.rframes[i] = pygame.transform.scale(self.rframes[i], (width, height))
            self.rframes[i] = self.rframes[i].convert_alpha()
        self.rect = self.frames["right"].get_rect()
        self.img = self.frames["right"]
        self.facing_right = True
        self.jumpFrameCount = 0
        self.jumpFrames = 2
        self.move_time = time.time() + 2 #temporary variable for moving enemies
        self.change_move = True  #temporary variable for moving enemies
        self.rect = self.img.get_rect()
        self.rect.midbottom = spawn_point
        self.pos.x, self.pos.y = self.rect.center
        self.alive = True
        self.cur_state = states.Falling
        self.onSurface = False
        self.stats["MAX_HP"] = 5
        self.stats["CUR_HP"] = self.stats["MAX_HP"]
        self.damage = 4
        self.invuln_timer = 0
        self.type = "ENEMY"
        self.sees_player = False

    def move(self, keys, dt):

        if self.sees_player:
            if self.facing_right:
                self.accel.x += PLAYER_ACC * 0.6
            else:
                self.accel.x -= PLAYER_ACC * 0.6

    def determineState(self):
       # if self.velocity.x < 0:
       #     self.facing_right = False
#
       # if self.velocity.x > 0:
       #     self.facing_right = True

        super().determineState()

    def update(self, *args):
        mouseButtons, keys, dt = args
        super().update(*args)

        if self.cur_state == states.Standing and self.facing_right:
            self.img = self.rframes[0]
        if self.cur_state == states.Standing and not self.facing_right:
            self.img = pygame.transform.flip(self.frames['right'], True, False)
        if self.cur_state == states.Running and self.facing_right:
            self.img = self.rframes[0]
        if self.cur_state == states.Running and not self.facing_right:
            self.img = pygame.transform.flip(self.frames['right'], True, False)

        if self.velocity.x == 0:
            self.facing_right = not self.facing_right
            self.accel = -self.accel

        self.move(keys,dt)

        self.invuln_timer -= dt

    def set_dead(self):
        """ Generic method for setting
            a enemy status to dead."""
        self.alive = False

    def line_of_sight(self, window, cameraPos, player, wallTiles):
        for tile in wallTiles:

            self.line = pygame.draw.line(window, (255, 255, 0), (int(self.rect.x - cameraPos[0]), int(self.rect.y - cameraPos[1])),
                                                (int(player.rect.x - cameraPos[0]), int(player.rect.y - cameraPos[1])))
            enex = int(self.rect.x - cameraPos[0])
            eney = int(self.rect.y - cameraPos[1])
            playx = int(player.rect.x - cameraPos[0])
            playy = int(player.rect.y - cameraPos[1])
            if ((enex-playx)**2) + ((eney-playy)**2) >= 150**2:
                vision_collision = False
                break
            if (enex - playx) == 0:
                vision_collision = False
                break
            lineSlope = (eney - playy)/(enex - playx)
            yintercept = eney+lineSlope*enex

            v1 = tile.rect.topleft
            v2 = tile.rect.topright
            v3 = tile.rect.bottomleft
            v4 = tile.rect.bottomright
            pygame.display.flip()
          #  startx, starty = self.rect.center
#
          #  line1 = pygame.draw.line(window, (255, 255, 0), (int(self.rect.x - cameraPos[0]), int(self.rect.y - cameraPos[1])),
          #                                      (int(v1[0] - cameraPos[0]), int(v1[1] - cameraPos[1])))
          #  line2 = pygame.draw.line(window, (255, 255, 0), (int(self.rect.x - cameraPos[0]), int(self.rect.y - cameraPos[1])),
          #                                      (int(v2[0] - cameraPos[0]), int(v2[1] - cameraPos[1])))
          #  line3 = pygame.draw.line(window, (255, 255, 0), (int(self.rect.x - cameraPos[0]), int(self.rect.y - cameraPos[1])),
          #                                      (int(v3[0] - cameraPos[0]), int(v3[1] - cameraPos[1])))
          #  line4 = pygame.draw.line(window, (255, 255, 0), (int(self.rect.x - cameraPos[0]), int(self.rect.y - cameraPos[1])),
          #                                      (int(v4[0] - cameraPos[0]), int(v4[1] - cameraPos[1])))

            if (v1[0]*lineSlope+yintercept) - v1[1] > 0 and v2[0]*lineSlope+yintercept - v2[1] > 0 and v3[0]*lineSlope+yintercept - v3[1] > 0 and v4[0]*lineSlope+yintercept - v4[1] > 0 or v1[0] * lineSlope + yintercept  - v1[1] < 0 and v2[0] * lineSlope + yintercept - v2[1] < 0 and v3[0] * lineSlope + yintercept - v3[1] < 0 and v4[0] * lineSlope + yintercept  - v4[1] < 0:
                vision_collision = True
                if int((player.rect.x - cameraPos[0])) > (int(self.rect.x - cameraPos[0])):
                    self.facing_right = True
                if int((player.rect.x - cameraPos[0])) < (int(self.rect.x - cameraPos[0])):
                    self.facing_right = False
            else:
                vision_collision = False
                break
        self.sees_player = vision_collision


    def take_damage(self, player):
        """Method that make the enemy take damage from an attack"""
        print("Enemy.py: Line 106: Current HP: ", self.stats["CUR_HP"])
        if self.stats["CUR_HP"] > 0 >= self.invuln_timer:
            if self.stats["CUR_HP"] - player.deal_dmg() <= 0:
                self.stats["CUR_HP"] = 0
                self.set_dead()
            else:
                self.stats["CUR_HP"] -= player.deal_dmg()
            self.invuln_timer = INVULN_TIMER

    def attack(self):
        """Method allows the enemy attack the player when in close enough range"""
        pass

    def draw(self, window, cameraPos):
        super().draw(window, cameraPos)
        window.blit(self.img, (int(self.rect.x - cameraPos[0]),int(self.rect.y - cameraPos[1])))
