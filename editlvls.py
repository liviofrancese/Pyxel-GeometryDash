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
        self.lvl_json_path = None
        self.camera_x = 0
        self.camera_y = 0

        #Level choosing
        self.choosing_level = 1
        self.choosen_obstacles = 'spike'
        self.choosen_placement = 'place'
        self.mouse_x = 0
        self.mouse_y = 0

        self.turned = False
        self.used = False

        self.no_place_obstacle = 0

        self.obstacles_temp = []
        self.end_of_level = None

        self.obstacles_pos = {
            'place': {'x': 1, 'y': self.game.screen_y-40},
            'delete': {'x': 1, 'y': self.game.screen_y-20},
            'spike': {'x': 20, 'y': self.game.screen_y-40},
            'turned spike': {'x': 20, 'y': self.game.screen_y-20},
            'block': {'x': 40, 'y': self.game.screen_y-40},
            'mur': {'x': 60, 'y': self.game.screen_y-40},
            'orb': {'x': 80, 'y': self.game.screen_y-40}
        }
      



    def quit_editor(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < 5+16 and pyxel.mouse_x > 5 and pyxel.mouse_y < 5+16 and pyxel.mouse_y > 5 or pyxel.btnp(pyxel.KEY_ESCAPE):
            self.in_editor = False
            self.game.menu = True
            self.no_place_obstacle = 0
            self.initialisation = False
            self.camera_x = 0
            self.camera_y = 0
            self.choosen_placement = 'place'
            self.game.menu_song_var = False
    def mouse_pos(self):
        self.mouse_x = pyxel.mouse_x
        self.mouse_y = pyxel.mouse_y
        if self.mouse_y >= self.game.cube_y_min+8:
            self.mouse_y = self.game.cube_y_min+8
    
    def choose_placement(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < self.obstacles_pos['place']['x']+16 and pyxel.mouse_x > self.obstacles_pos['place']['x'] and pyxel.mouse_y < self.obstacles_pos['place']['y']+16 and pyxel.mouse_y > self.obstacles_pos['place']['y']:
            self.choosen_placement = 'place'
            self.choosen_obstacles = 'spike'
            self.turned = False
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < self.obstacles_pos['delete']['x']+16 and pyxel.mouse_x > self.obstacles_pos['delete']['x'] and pyxel.mouse_y < self.obstacles_pos['delete']['y']+16 and pyxel.mouse_y > self.obstacles_pos['delete']['y']:
            self.choosen_placement = 'delete'
    
    def choose_obstacle(self):
        if self.choosen_placement == 'place':
            if (pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < self.obstacles_pos['spike']['x']+16 and pyxel.mouse_x > self.obstacles_pos['spike']['x'] and pyxel.mouse_y < self.obstacles_pos['spike']['y']+16 and pyxel.mouse_y > self.obstacles_pos['spike']['y']):
                self.choosen_obstacles = 'spike'
                self.turned = False
            elif (pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < self.obstacles_pos['turned spike']['x']+16 and pyxel.mouse_x > self.obstacles_pos['turned spike']['x'] and pyxel.mouse_y < self.obstacles_pos['turned spike']['y']+16 and pyxel.mouse_y > self.obstacles_pos['turned spike']['y']):
                self.choosen_obstacles = 'turned spike'
                self.turned = True
            elif (pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < self.obstacles_pos['block']['x']+16 and pyxel.mouse_x > self.obstacles_pos['block']['x'] and pyxel.mouse_y < self.obstacles_pos['block']['y']+16 and pyxel.mouse_y > self.obstacles_pos['block']['y']):
                self.choosen_obstacles = 'block'
                self.turned = False
            elif (pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < self.obstacles_pos['mur']['x']+16 and pyxel.mouse_x > self.obstacles_pos['mur']['x'] and pyxel.mouse_y < self.obstacles_pos['mur']['y']+16 and pyxel.mouse_y > self.obstacles_pos['mur']['y']):
                self.choosen_obstacles = 'mur'
                self.turned = False
            elif (pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < self.obstacles_pos['orb']['x']+16 and pyxel.mouse_x > self.obstacles_pos['orb']['x'] and pyxel.mouse_y < self.obstacles_pos['orb']['y']+16 and pyxel.mouse_y > self.obstacles_pos['orb']['y']):
                self.choosen_obstacles = 'orb'
                self.turned = False

    def editor_init(self):
        if not self.initialisation:
            self.game.reset_obstacles()
            self.obstacles_temp = self.game.obstacle_liste
            self.end_of_level = self.game.end_level
            self.initialisation = True
    def place_obstacle(self):
        if self.no_place_obstacle < 2:
            return
        if self.choosen_placement == 'place' and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_y-16 <= self.game.cube_y_min and not (pyxel.mouse_x < self.game.screen_x-11+8 and pyxel.mouse_x > self.game.screen_x-43-8 and pyxel.mouse_y < 20+10+8 and pyxel.mouse_y > 20-8) and not (pyxel.mouse_x < self.game.screen_x-4+8 and pyxel.mouse_x > self.game.screen_x-48-8 and pyxel.mouse_y < 8+10+8 and pyxel.mouse_y > 10-8):
            self.obstacles_temp.append({"x": self.mouse_x-8+self.camera_x, "y": self.mouse_y-8, "type": ('spike' if self.turned and self.choosen_obstacles == 'turned spike' else self.choosen_obstacles), "turned": self.turned, "used": self.used})

    def remove_obstacle(self):
        if self.choosen_placement == 'delete' and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            for obstacle in self.obstacles_temp:
                obstacle_x = obstacle['x']-self.camera_x
                obstacle_y = obstacle['y']-self.camera_y
                if pyxel.mouse_x >= obstacle_x and pyxel.mouse_x <= obstacle_x + 16 and pyxel.mouse_y >= obstacle_y and pyxel.mouse_y <= obstacle_y + 16:
                    self.obstacles_temp.remove(obstacle)
                    return
                    

    def write_json(self, file, data):
        with open (file, "w") as f:
            data = {"level_length": self.end_of_level, "obstacles": data}
            json.dump(data, f, indent=4)

    def saving(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < self.game.screen_x-4 and pyxel.mouse_x > self.game.screen_x-48 and pyxel.mouse_y < 8+10 and pyxel.mouse_y > 10:
            self.write_json(self.game.levels[self.game.current_level], self.obstacles_temp)
            self.lvl_json_path = self.game.levels[self.game.current_level]
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < self.game.screen_x-11 and pyxel.mouse_x > self.game.screen_x-43 and pyxel.mouse_y < 20+10 and pyxel.mouse_y > 20:
            while os.path.exists(self.custum_level):
                self.custum_level = f"levels\\custum_level{self.new_json_file}.json"
                self.new_json_file += 1
            self.write_json(self.custum_level, self.obstacles_temp)
            self.custum_level = "levels\\custum_level.json"
            self.new_json_file = 1
    def move_camera(self):
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.camera_x += 10
        if pyxel.btn(pyxel.KEY_LEFT):
            if not self.camera_x == 0:
                self.camera_x -= 10


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
    
    def draw_placement_to_choose(self):
        pyxel.blt(self.obstacles_pos['place']['x'], self.obstacles_pos['place']['y'], 1, 104, 0, 16, 16, 0)
        pyxel.blt(self.obstacles_pos['delete']['x'], self.obstacles_pos['delete']['y'], 1, 120, 0, 16, 16, 0)
        pyxel.rectb(self.obstacles_pos[self.choosen_placement]['x']-1, self.obstacles_pos[self.choosen_placement]['y']-1, 18, 18,2)
    
    def draw_obstacles_to_choose(self):
        #Spike
        pyxel.blt(self.obstacles_pos['spike']['x'], self.obstacles_pos['spike']['y'], self.game.obstacles_pyxres['spike']['image'], self.game.obstacles_pyxres['spike']['x'], self.game.obstacles_pyxres['spike']['y'], self.game.obstacles_pyxres['spike']['width'], self.game.obstacles_pyxres['spike']['height'], 0)
        #Turned spike
        pyxel.blt(self.obstacles_pos['turned spike']['x'], self.obstacles_pos['turned spike']['y'], self.game.obstacles_pyxres['turned spike']['image'], self.game.obstacles_pyxres['turned spike']['x'], self.game.obstacles_pyxres['turned spike']['y'], self.game.obstacles_pyxres['turned spike']['width'], self.game.obstacles_pyxres['turned spike']['height'], 0)
        #Block
        pyxel.blt(self.obstacles_pos['block']['x'], self.obstacles_pos['block']['y'], self.game.obstacles_pyxres['block']['image'], self.game.obstacles_pyxres['block']['x'], self.game.obstacles_pyxres['block']['y'], self.game.obstacles_pyxres['block']['width'], self.game.obstacles_pyxres['block']['height'], 0)
        #Mur
        pyxel.blt(self.obstacles_pos['mur']['x'], self.obstacles_pos['mur']['y'], self.game.obstacles_pyxres['mur']['image'], self.game.obstacles_pyxres['mur']['x'], self.game.obstacles_pyxres['mur']['y'], self.game.obstacles_pyxres['mur']['width'], self.game.obstacles_pyxres['mur']['height'], 0)
        #Orb
        pyxel.blt(self.obstacles_pos['orb']['x'], self.obstacles_pos['orb']['y'], self.game.obstacles_pyxres['orb']['image'], self.game.obstacles_pyxres['orb']['x'], self.game.obstacles_pyxres['orb']['y'], self.game.obstacles_pyxres['orb']['width'], self.game.obstacles_pyxres['orb']['height'], 0)
        #Choosen
        if self.choosen_placement == 'place' :
            pyxel.rectb(self.obstacles_pos[self.choosen_obstacles]['x']-2, self.obstacles_pos[self.choosen_obstacles]['y']-2, 20, 20, 10)    


    def draw_instructions(self):
        pyxel.text(self.game.screen_x/2+25, self.game.screen_y-8, f"Obstacle choisis: {self.choosen_obstacles}", 0)
        pyxel.text(self.game.screen_x/2+25, self.game.screen_y-18, "Fleches: Camera", 0)

    def editor_update(self):
        self.editor_init()
        self.no_place_obstacle += 1
        self.choose_placement()
        self.choose_obstacle()
        self.saving()
        self.mouse_pos()
        self.move_camera()
        self.place_obstacle()
        self.remove_obstacle()

        #Quit editor
        self.quit_editor()

    def editor_draw(self):
        pyxel.cls(1)
        #Bouton pour revenir au menu
        pyxel.blt(5, 5, 1, 48, 0, 16, 16,0)
        #Sol blanc
        pyxel.rect(0, self.game.cube_y_min+16, self.game.screen_x, self.game.screen_y, 7)

        self.draw_obstacles_to_choose()
        self.draw_placement_to_choose()
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
        if self.choosen_placement == 'place':
            pyxel.blt(self.mouse_x-8, self.mouse_y-8, self.game.obstacles_pyxres[self.choosen_obstacles]['image'], self.game.obstacles_pyxres[self.choosen_obstacles]['x'], self.game.obstacles_pyxres[self.choosen_obstacles]['y'], self.game.obstacles_pyxres[self.choosen_obstacles]['width'], self.game.obstacles_pyxres[self.choosen_obstacles]['height'], 0)

