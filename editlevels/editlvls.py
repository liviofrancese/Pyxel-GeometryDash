import pyxel
import json
import os
import subprocess

class LevelEditor:
    def __init__(self, game):
        #init all variables
        self.game = game
        self.in_editor = False

        self.edit_var_init = False
        self.quit = False

        #Level choosing
        self.choosing_level = 1


    def load_parameters(self):
        try:
            with open('window.json', 'r') as f:
                var_json = json.load(f)
                self.choosen_obstacles = var_json['choosen_obstacles']
        except:
            self.choosen_obstacles = 'spike'

    def window_quit(self):
        data = {
            "quit": True
        }
        with open(f"{self.game.folders['editlevels']}\\lvls.json", 'w') as f:
            json.dump(data, f, indent=4)

    def no_quit(self):
        data = {
            "quit": False
        }
        with open(f"{self.game.folders['editlevels']}\\lvls.json", 'w') as f:
            json.dump(data, f, indent=4)


    def editor_update(self):
        if not self.edit_var_init:
            self.no_quit()
            process = subprocess.Popen(["python", f"{self.game.folders['editlevels']}\\edit_window.py"])
            self.edit_var_init = True
        self.load_parameters()
        self.no_quit()
        #Menu 1: Choisir le niveau à éditer
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < 5+16 and pyxel.mouse_x > 5 and pyxel.mouse_y < 5+16 and pyxel.mouse_y > 5 or pyxel.btnp(pyxel.KEY_ESCAPE):
            self.in_editor = False
            self.edit_var_init = False
            self.window_quit()
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


