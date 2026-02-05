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

        


        pyxel.run(self.update, self.draw)







  

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
            pyxel.rectb(self.obstacles_pos['spike']['x']-2, self.obstacles_pos['spike']['y']-2, 20, 20, 10)
        pyxel.blt(self.obstacles_pos['spike']['x'], self.obstacles_pos['spike']['y'], self.obstacles_list['spike']['image'], self.obstacles_list['spike']['x'], self.obstacles_list['spike']['y'], self.obstacles_list['spike']['width'], self.obstacles_list['spike']['height'], 0)
        #Turned spike
        if self.editlvls.choosen_obstacles == 'turned spike':
            pyxel.rectb(self.obstacles_pos['turned spike']['x']-2, self.obstacles_pos['turned spike']['y']-2, 20, 20, 10)
        pyxel.blt(self.obstacles_pos['turned spike']['x'], self.obstacles_pos['turned spike']['y'], self.obstacles_list['turned spike']['image'], self.obstacles_list['turned spike']['x'], self.obstacles_list['turned spike']['y'], self.obstacles_list['turned spike']['width'], self.obstacles_list['turned spike']['height'], 0)
        #Block
        if self.editlvls.choosen_obstacles == 'block':
            pyxel.rectb(self.obstacles_pos['block']['x']-2, self.obstacles_pos['block']['y']-2, 20, 20, 10)
        pyxel.blt(self.obstacles_pos['block']['x'], self.obstacles_pos['block']['y'], self.obstacles_list['block']['image'], self.obstacles_list['block']['x'], self.obstacles_list['block']['y'], self.obstacles_list['block']['width'], self.obstacles_list['block']['height'], 0)
        #Mur
        if self.editlvls.choosen_obstacles == 'mur':
            pyxel.rectb(self.obstacles_pos['mur']['x']-2, self.obstacles_pos['mur']['y']-2, 20, 20, 10)
        pyxel.blt(self.obstacles_pos['mur']['x'], self.obstacles_pos['mur']['y'], self.obstacles_list['mur']['image'], self.obstacles_list['mur']['x'], self.obstacles_list['mur']['y'], self.obstacles_list['mur']['width'], self.obstacles_list['mur']['height'], 0)
        #Orb
        if self.editlvls.choosen_obstacles == 'orb':
            pyxel.rectb(self.obstacles_pos['orb']['x']-2, self.obstacles_pos['orb']['y']-2, 20, 20, 10)
        pyxel.blt(self.obstacles_pos['orb']['x'], self.obstacles_pos['orb']['y'], self.obstacles_list['orb']['image'], self.obstacles_list['orb']['x'], self.obstacles_list['orb']['y'], self.obstacles_list['orb']['width'], self.obstacles_list['orb']['height'], 0)
EditParameters()