import pyxel
import json
import os
import subprocess

class LevelEditor:
    def __init__(self, game):
        pyxel.mouse(True)
        #init all variables
        self.game = game
        self.in_editor = False
        self.hello = False
        self.edit_var_init = False
        self.quit = False

        #Level choosing
        self.choosing_level = 1



    def default_parameters(self):
        self.choosen_obstacles = 'spike'
        self.window_quit = False
        self.save_level = False
        self.save_as = False






    def editor_update(self):
        if not self.edit_var_init:
            process = subprocess.Popen(["python", f"{self.game.folders['editlevels']}\\edit_window.py"])
            self.edit_var_init = True


        #Quit editor
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < 5+16 and pyxel.mouse_x > 5 and pyxel.mouse_y < 5+16 and pyxel.mouse_y > 5 or pyxel.btnp(pyxel.KEY_ESCAPE):
            self.in_editor = False
            self.edit_var_init = False
            self.window_quit = True
            self.game.menu = True



    def editor_draw(self):
        pyxel.cls(1)
        #Bouton pour revenir au menu
        pyxel.blt(5, 5, 1, 48, 0, 16, 16,0)
        #Sol blanc
        pyxel.rect(0, self.game.cube_y_min+16, self.game.screen_x, self.game.screen_y, 7)
        
        #Niveau choisi
        if self.choosing_level == 1:
            pyxel.bltm(self.game.screen_x-135, 5, 0, 0, 32, 128, 32, 0)
        if self.choosing_level == 2:
            pyxel.bltm(self.game.screen_x-135, 5, 0, 0, 32, 128, 32, 0)


