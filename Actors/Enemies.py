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
        self.hp = 1
        self.damage = 4

    def move(self, keys, dt):
        if self.change_move:  #uncommenting this makes enemies walk left and right
            while time.time() > self.move_time:
                if self.accel.x < MAX_X_ACC:
                    self.accel.x += PLAYER_ACC
                self.change_move = False
                self.move_time = time.time() + 0.5
        elif not self.change_move:
            while time.time() > self.move_time:
                if self.accel.x > -MAX_X_ACC:
                    self.accel.x -= PLAYER_ACC
                self.change_move = True
                self.move_time = time.time() + 0.5

    def determineState(self):
        if self.velocity.x < 0:
            self.facing_right = False

        if self.velocity.x > 0:
            self.facing_right = True

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

        while time.time() > self.t_anim:
            self.anim += 1
            if self.anim > len(self.rframes)-1:
                self.anim = 0
            self.frames["right"] = self.rframes[self.anim]
            self.t_anim = time.time() + 0.125

    def set_dead(self):
        """ Generic method for setting
            a enemy status to dead."""
        self.alive = False

    def take_damage(self):
        """Method that make the enemy take damage from an attack"""
        self.hp -= 1
        if self.hp <= 0:
            self.set_dead()
        pass

    def attack(self):
        """Method allows the enemy attack the player when in close enough range"""
        pass

    def draw(self, window, cameraPos):
        super().draw(window, cameraPos)
        window.blit(self.img, (int(self.rect.x - cameraPos[0]),int(self.rect.y - cameraPos[1])))
