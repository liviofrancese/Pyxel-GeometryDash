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

        self.cube_pyxres = {
            'basic': {
                'image': 0,
                'x': 0,
                'y': 0,
                'width': 16,
                'height': 16
            },
            '2': {
                'image': 0,
                'x': 16,
                'y': 0,
                'width': 16,
                'height': 16
            },
            '3': {
                'image': 0,
                'x': 32,
                'y': 0,
                'width': 16,
                'height': 16
            },
            '4': {
                'image': 0,
                'x': 48,
                'y': 0,
                'width': 16,
                'height': 16
            }
        }

    def is_going_down(self):
        if not self.game.level.gravity_cube:
            if not self.going_down:
                self.cube_y_before = self.cube_y
                self.going_down = True
            elif self.going_down:
                self.cube_y_now = self.cube_y
                self.going_down = False
                if self.cube_y_before < self.cube_y_now:
                    self.game.level.jump = True

    def jump_rotation(self):
        #Saut du cube
        if pyxel.btn(pyxel.KEY_SPACE) and self.game.level.jump==False:
            self.game.level.jumping()
        if not self.game.level.gravity_cube:
            self.cube_y += self.game.level.velocity_y
            self.game.level.velocity_y += self.game.level.gravity
        if self.game.level.gravity_cube:
            self.cube_y -= self.game.level.velocity_y
            self.game.level.velocity_y -= self.game.level.gravity
        self.is_going_down()
        self.game.level.end -= self.game.level.speed

        if self.cube_rot:
            self.cube_rotation += 4
            if self.cube_rotation >= 80:
                self.cube_rotation = 0
        if self.game.level.jump==False:
            self.cube_rotation = 0
            self.cube_rot = False

        #Cube va au minimum au sol
        if not self.game.level.gravity_cube:
            if self.cube_y >= self.cube_y_min:
                self.cube_y = self.cube_y_min
                self.game.level.jump = False
                self.game.level.velocity_y = 0

    def draw_rotation_cube(self):
        if self.cube_rotation >= 0 and self.cube_rotation < 10:
            pyxel.blt(self.cube_x, self.cube_y, self.cube_pyxres['basic']['image'], self.cube_pyxres['basic']['x'], self.cube_pyxres['basic']['y'], self.cube_pyxres['basic']['width'], self.cube_pyxres['basic']['height'], 0)
        elif self.cube_rotation >= 10 and self.cube_rotation < 40:
            pyxel.blt(self.cube_x, self.cube_y, self.cube_pyxres['2']['image'], self.cube_pyxres['2']['x'], self.cube_pyxres['2']['y'], self.cube_pyxres['2']['width'], self.cube_pyxres['2']['height'], 0)
        elif self.cube_rotation >= 40 and self.cube_rotation < 50:
            pyxel.blt(self.cube_x, self.cube_y, self.cube_pyxres['3']['image'], self.cube_pyxres['3']['x'], self.cube_pyxres['3']['y'], self.cube_pyxres['3']['width'], self.cube_pyxres['3']['height'], 0)
        elif self.cube_rotation >= 50 and self.cube_rotation <= 80:
            pyxel.blt(self.cube_x, self.cube_y, self.cube_pyxres['4']['image'], self.cube_pyxres['4']['x'], self.cube_pyxres['4']['y'],  self.cube_pyxres['4']['width'], self.cube_pyxres['4']['height'], 0)