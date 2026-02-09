import pyxel

class Cube:
    def __init__(self, game):
        self.game = game

        self.cube_x = 40
        self.cube_x_pourc = 0
        self.cube_y_min = 140
        self.cube_y = self.cube_y_min
        self.y_min = self.cube_y_min
        self.cube_rotation = 0
        self.cube_rot = False
        #cube falling
        self.going_down = 0
        self.cube_y_before = 0
        self.cube_y_now = 0