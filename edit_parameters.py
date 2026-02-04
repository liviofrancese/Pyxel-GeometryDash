import pyxel
import json

class EditParameters:

    def __init__(self):
        self.screen_x = 300
        self.screen_y = 200
        pyxel.init(self.screen_x, self.screen_y, quit_key=pyxel.KEY_P, title="GeometryDash")
        pyxel.mouse(True)
        pyxel.load("geometrydash.pyxres")
        
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



        self.choosen_obstacles = 'spike'
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



    def write_parameters(self):
            data = {
                'choosen_obstacles': self.choosen_obstacles
            }
            with open('edit_var.json', 'w') as f:
                json.dump(data, f, indent=4)

    def choose_obstacle(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < self.x_spike+16 and pyxel.mouse_x > self.x_spike and pyxel.mouse_y < self.y_spike+16 and pyxel.mouse_y > self.y_spike:
            self.choosen_obstacles = 'spike'
        elif pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < self.x_turned_spike+16 and pyxel.mouse_x > self.x_turned_spike and pyxel.mouse_y < self.y_turned_spike+16 and pyxel.mouse_y > self.y_turned_spike:
            self.choosen_obstacles = 'turned spike'
        elif pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < self.x_block+16 and pyxel.mouse_x > self.x_block and pyxel.mouse_y < self.y_block+16 and pyxel.mouse_y > self.y_block:
            self.choosen_obstacles = 'block'
        elif pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < self.x_mur+16 and pyxel.mouse_x > self.x_mur and pyxel.mouse_y < self.y_mur+16 and pyxel.mouse_y > self.y_mur:
            self.choosen_obstacles = 'mur'
        elif pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < self.x_orb+16 and pyxel.mouse_x > self.x_orb and pyxel.mouse_y < self.y_orb+16 and pyxel.mouse_y > self.y_orb:
            self.choosen_obstacles = 'orb'

    def quit(self):
        try:
            with open('others_var.json', 'r') as f:
                data = json.load(f)
                if data['quit']:
                    pyxel.quit()
        except:
            pass


    def update(self):
        #Toujours avec les bons paramètres
        self.write_parameters()

        self.quit()

        #Choix obstacle
        self.choose_obstacle()


    def draw(self):
        pyxel.cls(7)
        pyxel.text(5, 10, "ESC: Quit", 0)
        pyxel.text(5, 20, "F1: Save Level", 0)
        pyxel.text(80, 10, "F2: Save As", 0)
        pyxel.text(80, 20, "T: Turn", 0)
        pyxel.text(155, 10, "Fleches: Camera", 0)
        pyxel.text(155, 20, "Click gauche: Ajouter/Supprimer", 0)

        pyxel.text(10, 50, f"Obstacle choisis: {self.choosen_obstacles}", 0)
        

        #Spike
        pyxel.blt(self.x_spike, self.y_spike, img=self.obstacles_list['spike']['image'], u=self.obstacles_list['spike']['x'], v=self.obstacles_list['spike']['y'], w=self.obstacles_list['spike']['width'], h=self.obstacles_list['spike']['height'], colkey=0)
        #Turned spike
        pyxel.blt(self.x_turned_spike, self.y_turned_spike, img=self.obstacles_list['turned spike']['image'], u=self.obstacles_list['turned spike']['x'], v=self.obstacles_list['turned spike']['y'], w=self.obstacles_list['turned spike']['width'], h=self.obstacles_list['turned spike']['height'], colkey=0)
        #Block
        pyxel.blt(self.x_block, self.y_block, img=self.obstacles_list['block']['image'], u=self.obstacles_list['block']['x'], v=self.obstacles_list['block']['y'], w=self.obstacles_list['block']['width'], h=self.obstacles_list['block']['height'], colkey=0)
        #Mur
        pyxel.blt(self.x_mur, self.y_mur, img=self.obstacles_list['mur']['image'], u=self.obstacles_list['mur']['x'], v=self.obstacles_list['mur']['y'], w=self.obstacles_list['mur']['width'], h=self.obstacles_list['mur']['height'], colkey=0)
        #Orb
        pyxel.blt(self.x_orb, self.y_orb, img=self.obstacles_list['orb']['image'], u=self.obstacles_list['orb']['x'], v=self.obstacles_list['orb']['y'], w=self.obstacles_list['orb']['width'], h=self.obstacles_list['orb']['height'], colkey=0)
EditParameters()