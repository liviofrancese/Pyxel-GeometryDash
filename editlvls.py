import pyxel
import json

class LevelEditor:
    def __init__(self, game):
        #init all variables
        self.game = game
        self.in_editor = False

        self.choosing_level = 1


    def load_parameters(self):
        with open('edit_valeurs.json', 'r') as f:
            var_json = json.load(f)
            self.choosen_obstacles = var_json['choosen_obstacles']



    def editor_update(self):
        self.load_parameters()
        #Menu 1: Choisir le niveau à éditer
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < 5+16 and pyxel.mouse_x > 5 and pyxel.mouse_y < 5+16 and pyxel.mouse_y > 5 or pyxel.btnp(pyxel.KEY_ESCAPE):
            self.in_editor = False
            self.game.menu = True



    def editor_draw(self):
        pyxel.cls(1)
        #Bouton pour revenir au menu
        pyxel.blt(5, 5, 1, 48, 0, 16, 16,0)
        #Sol blanc
        pyxel.rect(0, self.game.cube_y_min+16, self.game.screen_x, self.game.screen_y, 7)
        #Niveau choisi
        if self.choosing_level == 1:
            pyxel.bltm(self.game.screen_x-135, 5, 0, 0, 1*32, 128, 32, 0)
        if self.choosing_level == 2:
            pyxel.bltm(self.game.screen_x-135, 5, 0, 0, 2*32, 128, 32, 0)

        #Show obstacles (to click)
        #Spike-non tournée
        pyxel.blt(5, self.game.cube_y_min+30, 0, 16, 16, 16, 16, 0)

