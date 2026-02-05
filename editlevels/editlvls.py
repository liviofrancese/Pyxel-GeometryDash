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
            'spike': {'x': 5, 'y': self.game.screen_y-40},
            'turned spike': {'x': 5, 'y': self.game.screen_y-20},
            'block': {'x': 25, 'y': self.game.screen_y-40},
            'mur': {'x': 45, 'y': self.game.screen_y-40},
            'orb': {'x': 65, 'y': self.game.screen_y-40}
        }


    def default_parameters(self):
        self.choosen_obstacles = 'spike'

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

    def saving(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < self.game.screen_x-4 and pyxel.mouse_x > self.game.screen_x-48 and pyxel.mouse_y < 8+10 and pyxel.mouse_y > 10:
            print('Save Level')
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < self.game.screen_x-11 and pyxel.mouse_x > self.game.screen_x-43 and pyxel.mouse_y < 20+10 and pyxel.mouse_y > 20:
            print('Save As')



    def draw_obstacles_to_choose(self):
        #Spike
        if self.choosen_obstacles == 'spike':
            pyxel.rectb(self.obstacles_pos['spike']['x']-2, self.obstacles_pos['spike']['y']-2, 20, 20, 10)
        pyxel.blt(self.obstacles_pos['spike']['x'], self.obstacles_pos['spike']['y'], self.game.obstacles_list['spike']['image'], self.game.obstacles_list['spike']['x'], self.game.obstacles_list['spike']['y'], self.game.obstacles_list['spike']['width'], self.game.obstacles_list['spike']['height'], 0)
        #Turned spike
        if self.choosen_obstacles == 'turned spike':
            pyxel.rectb(self.obstacles_pos['turned spike']['x']-2, self.obstacles_pos['turned spike']['y']-2, 20, 20, 10)
        pyxel.blt(self.obstacles_pos['turned spike']['x'], self.obstacles_pos['turned spike']['y'], self.game.obstacles_list['turned spike']['image'], self.game.obstacles_list['turned spike']['x'], self.game.obstacles_list['turned spike']['y'], self.game.obstacles_list['turned spike']['width'], self.game.obstacles_list['turned spike']['height'], 0)
        #Block
        if self.choosen_obstacles == 'block':
            pyxel.rectb(self.obstacles_pos['block']['x']-2, self.obstacles_pos['block']['y']-2, 20, 20, 10)
        pyxel.blt(self.obstacles_pos['block']['x'], self.obstacles_pos['block']['y'], self.game.obstacles_list['block']['image'], self.game.obstacles_list['block']['x'], self.game.obstacles_list['block']['y'], self.game.obstacles_list['block']['width'], self.game.obstacles_list['block']['height'], 0)
        #Mur
        if self.choosen_obstacles == 'mur':
            pyxel.rectb(self.obstacles_pos['mur']['x']-2, self.obstacles_pos['mur']['y']-2, 20, 20, 10)
        pyxel.blt(self.obstacles_pos['mur']['x'], self.obstacles_pos['mur']['y'], self.game.obstacles_list['mur']['image'], self.game.obstacles_list['mur']['x'], self.game.obstacles_list['mur']['y'], self.game.obstacles_list['mur']['width'], self.game.obstacles_list['mur']['height'], 0)
        #Orb
        if self.choosen_obstacles == 'orb':
            pyxel.rectb(self.obstacles_pos['orb']['x']-2, self.obstacles_pos['orb']['y']-2, 20, 20, 10)
        pyxel.blt(self.obstacles_pos['orb']['x'], self.obstacles_pos['orb']['y'], self.game.obstacles_list['orb']['image'], self.game.obstacles_list['orb']['x'], self.game.obstacles_list['orb']['y'], self.game.obstacles_list['orb']['width'], self.game.obstacles_list['orb']['height'], 0)


    def editor_update(self):
        self.choose_obstacle()
        self.saving()
        #Quit editor
        self.quit_editor()


    def editor_draw(self):
        pyxel.cls(1)
        #Bouton pour revenir au menu
        pyxel.blt(5, 5, 1, 48, 0, 16, 16,0)
        #Sol blanc
        pyxel.rect(0, self.game.cube_y_min+16, self.game.screen_x, self.game.screen_y, 7)

        self.draw_obstacles_to_choose()
        pyxel.text(self.game.screen_x/2+25, self.game.screen_y-8, f"Obstacle choisis: {self.choosen_obstacles}", 0)
        pyxel.text(self.game.screen_x/2+25, self.game.screen_y-18, "Fleches: Camera", 0)
        pyxel.text(self.game.screen_x/2+25, self.game.screen_y-28, "Click gauche: Ajouter", 0)
        pyxel.text(self.game.screen_x/2+25, self.game.screen_y-38, "Click droit: Supprimer", 0)
        
        #Save Level
        pyxel.rect(self.game.screen_x-48, 8, 44, 10, 10)
        pyxel.text(self.game.screen_x-45, 10, "Save Level", 0)
        #Save As
        pyxel.rect(self.game.screen_x-43, 20, 32, 10, 10)
        pyxel.text(self.game.screen_x-40, 22, "Save As", 0)

        #Obstacle on mouse
        pyxel.blt(pyxel.mouse_x, pyxel.mouse_y, self.game.obstacles_list[self.choosen_obstacles]['image'], self.game.obstacles_list[self.choosen_obstacles]['x'], self.game.obstacles_list[self.choosen_obstacles]['y'], self.game.obstacles_list[self.choosen_obstacles]['width'], self.game.obstacles_list[self.choosen_obstacles]['height'], 0)

