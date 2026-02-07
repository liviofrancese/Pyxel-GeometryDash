import pyxel
import json
import os

class LevelEditor:
    def __init__(self, game):
        pyxel.mouse(True)
        #init all variables
        self.game = game
        self.in_editor = False
        self.new_json_file = 1
        self.custum_level = "levels\\custum_level.json"

        self.initialisation = False
        self.camera_x = 0
        self.camera_y = 0

        #Level choosing
        self.choosing_level = 1
        self.choosen_obstacles = 'spike'
        self.mouse_x = 0
        self.mouse_y = 0

        self.turned = False
        self.used = False

        self.no_place_obstacle = 0

        self.obstacles_temp = []

        self.obstacles_pos = {
            'spike': {'x': 5, 'y': self.game.screen_y-40},
            'turned spike': {'x': 5, 'y': self.game.screen_y-20},
            'block': {'x': 25, 'y': self.game.screen_y-40},
            'mur': {'x': 45, 'y': self.game.screen_y-40},
            'orb': {'x': 65, 'y': self.game.screen_y-40}
        }
      



    def quit_editor(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < 5+16 and pyxel.mouse_x > 5 and pyxel.mouse_y < 5+16 and pyxel.mouse_y > 5 or pyxel.btnp(pyxel.KEY_ESCAPE):
            self.in_editor = False
            self.game.menu = True
            self.no_place_obstacle = 0
            self.initialisation = False
            self.camera_x = 0
            self.camera_y = 0
            self.game.menu_song_var = False
    def mouse_pos(self):
        self.mouse_x = pyxel.mouse_x
        self.mouse_y = pyxel.mouse_y
        if self.mouse_y >= self.game.cube_y_min+8:
            self.mouse_y = self.game.cube_y_min+8
    def choose_obstacle(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < self.obstacles_pos['spike']['x']+16 and pyxel.mouse_x > self.obstacles_pos['spike']['x'] and pyxel.mouse_y < self.obstacles_pos['spike']['y']+16 and pyxel.mouse_y > self.obstacles_pos['spike']['y']:
            self.choosen_obstacles = 'spike'
            self.turned = False
        elif pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < self.obstacles_pos['turned spike']['x']+16 and pyxel.mouse_x > self.obstacles_pos['turned spike']['x'] and pyxel.mouse_y < self.obstacles_pos['turned spike']['y']+16 and pyxel.mouse_y > self.obstacles_pos['turned spike']['y']:
            self.choosen_obstacles = 'turned spike'
            self.turned = True
        elif pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < self.obstacles_pos['block']['x']+16 and pyxel.mouse_x > self.obstacles_pos['block']['x'] and pyxel.mouse_y < self.obstacles_pos['block']['y']+16 and pyxel.mouse_y > self.obstacles_pos['block']['y']:
            self.choosen_obstacles = 'block'
            self.turned = False
        elif pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < self.obstacles_pos['mur']['x']+16 and pyxel.mouse_x > self.obstacles_pos['mur']['x'] and pyxel.mouse_y < self.obstacles_pos['mur']['y']+16 and pyxel.mouse_y > self.obstacles_pos['mur']['y']:
            self.choosen_obstacles = 'mur'
            self.turned = False
        elif pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < self.obstacles_pos['orb']['x']+16 and pyxel.mouse_x > self.obstacles_pos['orb']['x'] and pyxel.mouse_y < self.obstacles_pos['orb']['y']+16 and pyxel.mouse_y > self.obstacles_pos['orb']['y']:
            self.choosen_obstacles = 'orb'
            self.turned = False

    def editor_init(self):
        if not self.initialisation:
            self.game.reset_obstacles()
            self.obstacles_temp = self.game.obstacle_liste
            self.initialisation = True
    def place_obstacle(self):
        if self.no_place_obstacle < 2:
            return
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_y-16 <= self.game.cube_y_min and not (pyxel.mouse_x < self.game.screen_x-11+8 and pyxel.mouse_x > self.game.screen_x-43-8 and pyxel.mouse_y < 20+10+8 and pyxel.mouse_y > 20-8) and not (pyxel.mouse_x < self.game.screen_x-4+8 and pyxel.mouse_x > self.game.screen_x-48-8 and pyxel.mouse_y < 8+10+8 and pyxel.mouse_y > 10-8):
            self.obstacles_temp.append({"x": self.mouse_x-8+self.camera_x, "y": self.mouse_y-8, "type": self.choosen_obstacles, "turned": self.turned, "used": self.used})
    def remove_obstacle(self):
        pass
    def saving(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < self.game.screen_x-4 and pyxel.mouse_x > self.game.screen_x-48 and pyxel.mouse_y < 8+10 and pyxel.mouse_y > 10:
            print('Save Level')
            print(self.no_place_obstacle)
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < self.game.screen_x-11 and pyxel.mouse_x > self.game.screen_x-43 and pyxel.mouse_y < 20+10 and pyxel.mouse_y > 20:
            print('Save As')
            while os.path.exists(self.custum_level):
                self.custum_level = f"levels\\custum_level{self.new_json_file}.json"
                self.new_json_file += 1

            with open (self.custum_level, "w") as f:
                data = self.obstacles_temp
                json.dump(data, f, indent=3)
            self.custum_level = "levels\\custum_level.json"
            self.new_json_file = 1
    def move_camera(self):
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.camera_x += 5
        if pyxel.btn(pyxel.KEY_LEFT):
            if not self.camera_x == 0:
                self.camera_x -= 5

    def draw_obstacles(self):
        for obstacle in self.obstacles_temp:
            if obstacle['x']-self.camera_x < self.game.screen_x:
                if obstacle['type']=='spike' and obstacle['turned']==False:
                    pyxel.blt(obstacle['x']-self.camera_x, obstacle['y'], 0, 16, 16, 16, 16, 0)
                if obstacle['type']=='spike' and obstacle['turned']==True:
                    pyxel.blt(obstacle['x']-self.camera_x, obstacle['y'], 0, 16, 32, 16, 16, 0)
                if obstacle['type']=='block':
                    pyxel.blt(obstacle['x']-self.camera_x, obstacle['y'], 0, 32, 16, 16, 16)
                if obstacle['type']=='mur':
                    pyxel.blt(obstacle['x']-self.camera_x, obstacle['y'], 0, 0, 16, 16, 16)
                if obstacle['type']=='orb':
                    pyxel.blt(obstacle['x']-self.camera_x, obstacle['y'], 0, 48, 16, 16, 16, 0)
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
    def draw_instructions(self):
        pyxel.text(self.game.screen_x/2+25, self.game.screen_y-8, f"Obstacle choisis: {self.choosen_obstacles}", 0)
        pyxel.text(self.game.screen_x/2+25, self.game.screen_y-18, "Fleches: Camera", 0)
        pyxel.text(self.game.screen_x/2+25, self.game.screen_y-28, "Click gauche: Ajouter", 0)
        pyxel.text(self.game.screen_x/2+25, self.game.screen_y-38, "Click droit: Supprimer", 0)

    def editor_update(self):
        self.editor_init()
        self.no_place_obstacle += 1
        self.choose_obstacle()
        self.saving()
        self.mouse_pos()
        self.move_camera()
        self.place_obstacle()

        #Quit editor
        self.quit_editor()

    def editor_draw(self):
        pyxel.cls(1)
        #Bouton pour revenir au menu
        pyxel.blt(5, 5, 1, 48, 0, 16, 16,0)
        #Sol blanc
        pyxel.rect(0, self.game.cube_y_min+16, self.game.screen_x, self.game.screen_y, 7)

        self.draw_obstacles_to_choose()
        self.draw_instructions()
        
        #Save Level
        pyxel.rect(self.game.screen_x-48, 8, 44, 10, 10)
        pyxel.text(self.game.screen_x-45, 10, "Save Level", 0)
        #Save As
        pyxel.rect(self.game.screen_x-43, 20, 32, 10, 10)
        pyxel.text(self.game.screen_x-40, 22, "Save As", 0)
        #Camera
        pyxel.text(self.game.screen_x/2+50, 5, f"Camera: {self.camera_x}",7)

        self.draw_obstacles()

        #Obstacle on mouse
        pyxel.blt(self.mouse_x-8, self.mouse_y-8, self.game.obstacles_list[self.choosen_obstacles]['image'], self.game.obstacles_list[self.choosen_obstacles]['x'], self.game.obstacles_list[self.choosen_obstacles]['y'], self.game.obstacles_list[self.choosen_obstacles]['width'], self.game.obstacles_list[self.choosen_obstacles]['height'], 0)

