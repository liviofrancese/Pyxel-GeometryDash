import pyxel
import json
import os

class LevelEditor:
    def __init__(self, game):
        pyxel.mouse(True)
        self.game = game
        #init all variables
        self.in_editor = False
        self.new_json_file = 1
        self.custum_level = f"{self.game.folders['levels']}\\custum_level.json"

        self.initialisation = False
        self.camera_x = 0
        self.camera_y = 0

        #Level choosing
        self.choosing_level = 1
        self.choosen_obstacles = 'spike'
        self.choosen_placement = 'place'
        self.mouse_x = 0
        self.mouse_y = 0

        self.turned = False

        self.no_place_obstacle = 0

        self.obstacles_temp = []
        self.end_of_level = None
        self.lvl_name = ""
        self.lvl_name_text = ""
        self.save_as_text = False
        self.lvl_already_exists = False
        self.exists_timer = 0

        self.obstacles_pos = {
            'place': {'x': 1, 'y': self.game.screen_y-40},
            'delete': {'x': 1, 'y': self.game.screen_y-20},
            'spike': {'x': 20, 'y': self.game.screen_y-40},
            'turned spike': {'x': 20, 'y': self.game.screen_y-20},
            'block': {'x': 40, 'y': self.game.screen_y-40},
            'mur': {'x': 60, 'y': self.game.screen_y-40},
            'orb': {'x': 80, 'y': self.game.screen_y-40},
            'jump pad': {'x': 80, 'y': self.game.screen_y-20},
            'gravity orb': {'x': 100, 'y': self.game.screen_y-40},
            'small spike': {'x': 40, 'y': self.game.screen_y-20},
        }
      


                



    def save_as(self):
        if self.save_as_text:
            if pyxel.input_text:
                self.lvl_name_text += pyxel.input_text
            if pyxel.btnp(pyxel.KEY_BACKSPACE) and len(self.lvl_name_text) > 0:
                self.lvl_name_text = self.lvl_name_text[:-1]
            if pyxel.btnp(pyxel.KEY_KP_ENTER) or pyxel.btnp(pyxel.KEY_RETURN):
                self.lvl_name = f"{self.game.folders['levels']}\\{self.lvl_name_text}.json"
                print(self.lvl_name)
                if os.path.exists(self.lvl_name):
                    self.lvl_already_exists = True
                    return
                
                if self.lvl_name == "":
                    self.lvl_name = self.custum_level
                    while os.path.exists(self.lvl_name):
                        self.lvl_name = f"levels\\custum_level{self.new_json_file}.json"
                        self.new_json_file += 1
                
                self.write_json(self.lvl_name, self.obstacles_temp)
                self.new_json_file = 1
                self.save_as_text = False
                self.lvl_name_text = ""
        
        if self.lvl_already_exists:
            self.exists_timer +=1
            if self. exists_timer >= 50:
                self.lvl_already_exists = False
    def draw_save_as(self):
        if self.save_as_text:
            pyxel.text(self.game.screen_x/2-80, self.game.screen_y/2-63, "Level name:", 7)
            pyxel.text(self.game.screen_x/2-80, self.game.screen_y/2-55, f"{self.lvl_name_text}_", 7)
            if self.lvl_already_exists:
                pyxel.text(self.game.screen_x/2-80, self.game.screen_y/2+-47, "Level already exists", 2)

    def quit_editor(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < 5+16 and pyxel.mouse_x > 5 and pyxel.mouse_y < 5+16 and pyxel.mouse_y > 5 or pyxel.btnp(pyxel.KEY_ESCAPE):
            self.in_editor = False
            self.game.menu.in_menu = True
            self.no_place_obstacle = 0
            self.initialisation = False
            self.camera_x = 0
            self.camera_y = 0
            self.choosen_placement = 'place'
            self.game.menu.menu_song_var = False
            self.save_as_text = False
            self.lvl_already_exists = False
    def mouse_pos(self):
        self.mouse_x = pyxel.mouse_x
        self.mouse_y = pyxel.mouse_y
        if self.mouse_y >= self.game.cube.cube_y_min+8:
            self.mouse_y = self.game.cube.cube_y_min+8
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
            elif (pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < self.obstacles_pos['jump pad']['x']+16 and pyxel.mouse_x > self.obstacles_pos['jump pad']['x'] and pyxel.mouse_y < self.obstacles_pos['jump pad']['y']+16 and pyxel.mouse_y > self.obstacles_pos['jump pad']['y']):
                self.choosen_obstacles = 'jump pad'
                self.turned = False
            elif (pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < self.obstacles_pos['gravity orb']['x']+16 and pyxel.mouse_x > self.obstacles_pos['gravity orb']['x'] and pyxel.mouse_y < self.obstacles_pos['gravity orb']['y']+16 and pyxel.mouse_y > self.obstacles_pos['gravity orb']['y']):
                self.choosen_obstacles = 'gravity orb'
                self.turned = False
            elif (pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < self.obstacles_pos['small spike']['x']+16 and pyxel.mouse_x > self.obstacles_pos['small spike']['x'] and pyxel.mouse_y < self.obstacles_pos['small spike']['y']+16 and pyxel.mouse_y > self.obstacles_pos['small spike']['y']):
                self.choosen_obstacles = 'small spike'
                self.turned = False
    def editor_init(self):
        if not self.initialisation:
            self.game.level.reset_obstacles()
            self.obstacles_temp = self.game.level.obstacle_liste
            self.end_of_level = self.game.level.end
            self.initialisation = True
    def place_obstacle(self):
        if self.no_place_obstacle < 2:
            return
        if self.choosen_placement == 'place' and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_y-16 <= self.game.cube.cube_y_min and not (pyxel.mouse_x < self.game.screen_x-11+8 and pyxel.mouse_x > self.game.screen_x-43-8 and pyxel.mouse_y < 20+10+8 and pyxel.mouse_y > 20-8) and not (pyxel.mouse_x < self.game.screen_x-4+8 and pyxel.mouse_x > self.game.screen_x-48-8 and pyxel.mouse_y < 8+10+8 and pyxel.mouse_y > 10-8):
            self.obstacles_temp.append({"x": self.mouse_x-8+self.camera_x, "y": self.mouse_y-8, "type": self.choosen_obstacles})
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
            self.write_json(self.game.levels[self.game.level.current_level], self.obstacles_temp)
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < self.game.screen_x-11 and pyxel.mouse_x > self.game.screen_x-43 and pyxel.mouse_y < 20+10 and pyxel.mouse_y > 20:
            self.save_as_text = True


    def move_camera(self):
        if pyxel.btnp(pyxel.KEY_UP):
            self.camera_x = self.end_of_level-self.game.screen_x+50
        if pyxel.btnp(pyxel.KEY_DOWN):
            self.camera_x = 0
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.camera_x += 10
        if pyxel.btn(pyxel.KEY_LEFT):
            if not self.camera_x == 0:
                self.camera_x -= 10


    def draw_obstacles(self):
        for obstacle in self.obstacles_temp:
            if obstacle['x']-self.camera_x < self.game.screen_x:
                pyxel.blt(obstacle['x']-self.camera_x, obstacle['y'], self.game.level.obstacles_pyxres[obstacle['type']]['image'], self.game.level.obstacles_pyxres[obstacle['type']]['x'], self.game.level.obstacles_pyxres[obstacle['type']]['y'], self.game.level.obstacles_pyxres[obstacle['type']]['width'], self.game.level.obstacles_pyxres[obstacle['type']]['height'], 0)

        #Finish line
        if len(self.obstacles_temp) > 0:
            self.end_of_level = max(obstacle['x'] for obstacle in self.obstacles_temp)+25
            if self.end_of_level-self.camera_x < self.game.screen_x:
                pyxel.line(self.end_of_level-self.camera_x, 0, self.end_of_level-self.camera_x, self.game.cube.cube_y_min+16, 4)
    
    def draw_placement_to_choose(self):
        pyxel.blt(self.obstacles_pos['place']['x'], self.obstacles_pos['place']['y'], 1, 104, 0, 16, 16, 0)
        pyxel.blt(self.obstacles_pos['delete']['x'], self.obstacles_pos['delete']['y'], 1, 120, 0, 16, 16, 0)
        pyxel.rectb(self.obstacles_pos[self.choosen_placement]['x']-1, self.obstacles_pos[self.choosen_placement]['y']-1, 18, 18,2)
    
    def draw_obstacles_to_choose(self):
        for obstacle in self.game.level.obstacles_pyxres:
            pyxel.blt(self.obstacles_pos[obstacle]['x'], self.obstacles_pos[obstacle]['y'], self.game.level.obstacles_pyxres[obstacle]['image'], self.game.level.obstacles_pyxres[obstacle]['x'], self.game.level.obstacles_pyxres[obstacle]['y'], self.game.level.obstacles_pyxres[obstacle]['width'], self.game.level.obstacles_pyxres[obstacle]['height'], 0)

        #Choosen
        if self.choosen_placement == 'place' :
            pyxel.rectb(self.obstacles_pos[self.choosen_obstacles]['x']-2, self.obstacles_pos[self.choosen_obstacles]['y']-2, 20, 20, 10)

    def editor_update(self):
        if self.in_editor:
            self.editor_init()
            self.no_place_obstacle += 1
            self.choose_placement()
            self.choose_obstacle()
            #Save
            self.saving()
            self.save_as()

            self.mouse_pos()
            self.move_camera()
            self.place_obstacle()
            self.remove_obstacle()

            #Quit editor
            self.quit_editor()

    def editor_draw(self):
        if self.in_editor:
            pyxel.cls(1)
            
            #Sol blanc
            pyxel.rect(0, self.game.cube.cube_y_min+16, self.game.screen_x, self.game.screen_y, 7)

            self.draw_obstacles_to_choose()
            self.draw_placement_to_choose()
            self.draw_obstacles()
            
            #Save Level
            pyxel.rect(self.game.screen_x-48, 8, 44, 10, 10)
            pyxel.text(self.game.screen_x-45, 10, "Save Level", 0)
            #Save As
            pyxel.rect(self.game.screen_x-43, 20, 32, 10, 10)
            pyxel.text(self.game.screen_x-40, 22, "Save As", 0)
            #Camera
            pyxel.text(self.game.screen_x/2+50, 5, f"Camera: {self.camera_x}",7)

            pyxel.text(30, 5, f"Obstacle choisis: {self.choosen_obstacles}", 7)
            pyxel.text(self.game.screen_x-65, self.game.cube.cube_y_min+22, "Fleches: Camera", 0)

            #Obstacle on mouse
            if self.choosen_placement == 'place':
                pyxel.blt(self.mouse_x-8, self.mouse_y-8, self.game.level.obstacles_pyxres[self.choosen_obstacles]['image'], self.game.level.obstacles_pyxres[self.choosen_obstacles]['x'], self.game.level.obstacles_pyxres[self.choosen_obstacles]['y'], self.game.level.obstacles_pyxres[self.choosen_obstacles]['width'], self.game.level.obstacles_pyxres[self.choosen_obstacles]['height'], 0)

            self.draw_save_as()

            #Bouton pour revenir au menu
            pyxel.blt(5, 5, 1, 48, 0, 16, 16,0)