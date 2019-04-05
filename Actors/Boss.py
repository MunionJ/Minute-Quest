from Actors.Enemies import Enemy

class Boss(Enemy):

    def __init__(self, spawn_point, img, xp_val=100):
        """

        :param spawn_point: x,y position in world to place boss
        :param img: filename of boss sprite
        :param xp_val: xp value of boss to award players upon defeat
        """
        super().__init__()

    def update(self, *args):
        """

        :param args: mouseButtons, keys, dt, projectiles
        :return: void
        """
        super().update(*args)

    def draw(self,window,cameraPos):
        """
        :param window: window to blit image to
        :param cameraPos: offset of world position to place sprite on screen
        :return:
        """
        super().draw(window,cameraPos)

