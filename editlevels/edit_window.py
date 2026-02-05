import pyxel
import os
from editlvls import LevelEditor

class EditParameters:

    def __init__(self):
        self.screen_x = 300
        self.screen_y = 200
        pyxel.init(self.screen_x, self.screen_y, quit_key=pyxel.KEY_P, title="GeometryDash")
        pyxel.mouse(True)
        self.editlvls = LevelEditor(self)
        #geometrydash.pyxres qui se trouve dans le dossier parent
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        pyxres_path = os.path.join(parent_dir, "geometrydash.pyxres")
        pyxel.load(pyxres_path)
        
        self.x_spike=10
        self.y_spike=80
        self.x_turned_spike=10
        self.y_turned_spike=100
        self.x_block=30
        self.y_block=80
        self.x_mur=50
        self.y_mur=80
        self.x_orb=70
        self.y_orb=80





        self.obstacles_list = {
            'spike': {
                'image': 0,
                'x': 16,
                'y': 16,
                'width': 16,
                'height': 16
            },
            'turned spike': {
                'image': 0,
                'x': 16,
                'y': 32,
                'width': 16,
                'height': 16
            },
            'block': {
                'image': 0,
                'x': 32,
                'y': 16,
                'width': 16,
                'height': 16
            },
            'mur': {
                'image': 0,
                'x': 0,
                'y': 16,
                'width': 16,
                'height': 16
            },
            'orb': {
                'image': 0,
                'x': 48,
                'y': 16,
                'width': 16,
                'height': 16
            }
        }


        pyxel.run(self.update, self.draw)




    def choose_obstacle(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < self.x_spike+16 and pyxel.mouse_x > self.x_spike and pyxel.mouse_y < self.y_spike+16 and pyxel.mouse_y > self.y_spike:
            self.editlvls.choosen_obstacles = 'spike'
        elif pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < self.x_turned_spike+16 and pyxel.mouse_x > self.x_turned_spike and pyxel.mouse_y < self.y_turned_spike+16 and pyxel.mouse_y > self.y_turned_spike:
            self.editlvls.choosen_obstacles = 'turned spike'
        elif pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < self.x_block+16 and pyxel.mouse_x > self.x_block and pyxel.mouse_y < self.y_block+16 and pyxel.mouse_y > self.y_block:
            self.editlvls.choosen_obstacles = 'block'
        elif pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < self.x_mur+16 and pyxel.mouse_x > self.x_mur and pyxel.mouse_y < self.y_mur+16 and pyxel.mouse_y > self.y_mur:
            self.editlvls.choosen_obstacles = 'mur'
        elif pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < self.x_orb+16 and pyxel.mouse_x > self.x_orb and pyxel.mouse_y < self.y_orb+16 and pyxel.mouse_y > self.y_orb:
            self.editlvls.choosen_obstacles = 'orb'


  

    def saving(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < 3+44 and pyxel.mouse_x > 3 and pyxel.mouse_y < 8+10 and pyxel.mouse_y > 10:
            self.editlvls.save_level = True
            print('Save Level')
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < 3+32 and pyxel.mouse_x > 3 and pyxel.mouse_y < 20+10 and pyxel.mouse_y > 20:
            self.editlvls.save_as = True
            print('Save As')


    def update(self):
        #Choix obstacle
        self.choose_obstacle()

        #Save
        self.saving()

        #Quit
        if self.editlvls.window_quit:
             pyxel.quit()

        


    def draw(self):
        pyxel.cls(7)
        #Save Level
        pyxel.rect(3, 8, 44, 10, 10)
        pyxel.text(5, 10, "Save Level", 0)
        #Save As
        pyxel.rect(3, 20, 32, 10, 10)
        pyxel.text(5, 22, "Save As", 0)
        pyxel.text(155, 10, "Fleches: Camera", 0)
        pyxel.text(155, 20, "Click gauche: Ajouter/Supprimer", 0)

        pyxel.text(10, 50, f"Obstacle choisis: {self.editlvls.choosen_obstacles}", 0)
        

        #Spike
        if self.editlvls.choosen_obstacles == 'spike':
            pyxel.rectb(self.x_spike-2, self.y_spike-2, 20, 20, 10)
        pyxel.blt(self.x_spike, self.y_spike, self.obstacles_list['spike']['image'], self.obstacles_list['spike']['x'], self.obstacles_list['spike']['y'], self.obstacles_list['spike']['width'], self.obstacles_list['spike']['height'], 0)
        #Turned spike
        if self.editlvls.choosen_obstacles == 'turned spike':
            pyxel.rectb(self.x_turned_spike-2, self.y_turned_spike-2, 20, 20, 10)
        pyxel.blt(self.x_turned_spike, self.y_turned_spike, self.obstacles_list['turned spike']['image'], self.obstacles_list['turned spike']['x'], self.obstacles_list['turned spike']['y'], self.obstacles_list['turned spike']['width'], self.obstacles_list['turned spike']['height'], 0)
        #Block
        if self.editlvls.choosen_obstacles == 'block':
            pyxel.rectb(self.x_block-2, self.y_block-2, 20, 20, 10)
        pyxel.blt(self.x_block, self.y_block, self.obstacles_list['block']['image'], self.obstacles_list['block']['x'], self.obstacles_list['block']['y'], self.obstacles_list['block']['width'], self.obstacles_list['block']['height'], 0)
        #Mur
        if self.editlvls.choosen_obstacles == 'mur':
            pyxel.rectb(self.x_mur-2, self.y_mur-2, 20, 20, 10)
        pyxel.blt(self.x_mur, self.y_mur, self.obstacles_list['mur']['image'], self.obstacles_list['mur']['x'], self.obstacles_list['mur']['y'], self.obstacles_list['mur']['width'], self.obstacles_list['mur']['height'], 0)
        #Orb
        if self.editlvls.choosen_obstacles == 'orb':
            pyxel.rectb(self.x_orb-2, self.y_orb-2, 20, 20, 10)
        pyxel.blt(self.x_orb, self.y_orb, self.obstacles_list['orb']['image'], self.obstacles_list['orb']['x'], self.obstacles_list['orb']['y'], self.obstacles_list['orb']['width'], self.obstacles_list['orb']['height'], 0)
EditParameters()