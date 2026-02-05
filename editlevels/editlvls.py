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
        self.quit = False

        #Level choosing
        self.choosing_level = 1
        self.default_parameters()

        self.obstacles_pos = {
            'spike': {'x': 10, 'y': 80},
            'turned spike': {'x': 10, 'y': 100},
            'block': {'x': 30, 'y': 80},
            'mur': {'x': 50, 'y': 80},
            'orb': {'x': 70, 'y':80}
        }


    def default_parameters(self):
        self.choosen_obstacles = 'spike'
        self.save_level = False
        self.save_as = False


    def quit_editor(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < 5+16 and pyxel.mouse_x > 5 and pyxel.mouse_y < 5+16 and pyxel.mouse_y > 5 or pyxel.btnp(pyxel.KEY_ESCAPE):
            self.in_editor = False
            self.game.menu = True

    def choose_obstacle(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < self.obstacles_pos['spike']['x']+16 and pyxel.mouse_x > self.obstacles_pos['spike']['x'] and pyxel.mouse_y < self.obstacles_pos['spike']['y']+16 and pyxel.mouse_y > self.obstacles_pos['spike']['y']:
            self.choosen_obstacles = 'spike'
        elif pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < self.obstacles_pos['turned spike']['x']+16 and pyxel.mouse_x > self.obstacles_pos['turned spike']['x'] and pyxel.mouse_y < self.obstacles_pos['turned spike']['y']+16 and pyxel.mouse_y > self.obstacles_pos['turned spike']['y']:
            self.choosen_obstacles = 'turned spike'
        elif pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < self.obstacles_pos['block']['x']+16 and pyxel.mouse_x > self.obstacles_pos['block']['x'] and pyxel.mouse_y < self.obstacles_pos['block']['y']+16 and pyxel.mouse_y > self.obstacles_pos['block']['y']:
            self.choosen_obstacles = 'block'
        elif pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < self.obstacles_pos['mur']['x']+16 and pyxel.mouse_x > self.obstacles_pos['mur']['x'] and pyxel.mouse_y < self.obstacles_pos['mur']['y']+16 and pyxel.mouse_y > self.obstacles_pos['mur']['y']:
            self.choosen_obstacles = 'mur'
        elif pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < self.obstacles_pos['orb']['x']+16 and pyxel.mouse_x > self.obstacles_pos['orb']['x'] and pyxel.mouse_y < self.obstacles_pos['orb']['y']+16 and pyxel.mouse_y > self.obstacles_pos['orb']['y']:
            self.choosen_obstacles = 'orb'

    def editor_update(self):
        self.choose_obstacle()
        #Quit editor
        self.quit_editor()


    def editor_draw(self):
        pyxel.cls(1)
        #Bouton pour revenir au menu
        pyxel.blt(5, 5, 1, 48, 0, 16, 16,0)
        #Sol blanc
        pyxel.rect(0, self.game.cube_y_min+16, self.game.screen_x, self.game.screen_y, 7)

        #Obstacle on mouse
        pyxel.blt(pyxel.mouse_x, pyxel.mouse_y, self.game.obstacles_list[self.choosen_obstacles]['image'], self.game.obstacles_list[self.choosen_obstacles]['x'], self.game.obstacles_list[self.choosen_obstacles]['y'], self.game.obstacles_list[self.choosen_obstacles]['width'], self.game.obstacles_list[self.choosen_obstacles]['height'], 0)

