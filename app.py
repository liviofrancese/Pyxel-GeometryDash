import pyxel
import json
import os
from editlvls import LevelEditor
from menu import Menu
from cube import Cube
from cheats import Cheats
from level import Level
from music import Music


class Game:
    def __init__(self):
        self.screen_x = 300
        self.screen_y = 200
        pyxel.init(self.screen_x, self.screen_y, quit_key=pyxel.KEY_P, title="GeometryDash")
        pyxel.mouse(True)
        pyxel.load("geometrydash.pyxres")

        #Class
        self.level_editor = LevelEditor(self)
        self.menu = Menu(self)
        self.cube = Cube(self)
        self.cheats = Cheats(self)
        self.level = Level(self)
        self.music = Music(self)

        self.folders = {
            "default": os.getcwd(),
            "levels": f"{os.getcwd()}\\levels",
            "editlevels": f"{os.getcwd()}\\editlevels"
        }


        self.levels_json()


        pyxel.run(self.update, self.draw)




    def levels_json(self):
        #Fichiers où se trouvent les niveaux
        levels_folder = f"{os.getcwd()}\\levels"
        self.levels = {}
        for filename in os.listdir(levels_folder):
            if filename.endswith(".json") and filename.startswith("lvl"):
                #Créer une variable avec l'emplacement du fichier.json
                var_name = filename.replace(".json", "")
                self.levels[var_name] = f"{levels_folder}\\{filename}"
                self.menu.chosen_level_max += 1

    def default_var(self):
        #music
        self.menu.menu_song_var = False
        self.level.death_sound_var = False
        self.level.music_position = None
        self.level.sound = 0
        self.level.sec = 0
        self.level.sec_list = [0] * 64

        #cube
        self.cube.cube_y = self.cube.cube_y_min
        self.level.velocity_y = 0
        self.level.speed = self.level.velocity_x
        self.level.jump = False
        self.level.game_over = False
        self.level.finish = False

        #game
        self.level.initialisation = False
        self.level.ESC_level = False
        #Pourcentage
        self.level.end_pourc = self.level.end
        self.cube.cube_x_pourc = 0








    #level update et draw
    def niveau_update(self):
        if self.level.in_level:
            #Level initialization
            self.level.level_init()

            #Get song position
            self.music.get_song_pos()

            #Gestion d'obstacles
            self.level.obstacles_gestion()

            #Obstacles:
            self.level.deplacement_obstacles()

            #Pourcentage du niveau:
            self.level.level_pourc()

            #Gestion du cube
            self.level.cube_jump_rot()

            #ESC
            self.level.ESC()

            #endlevel
            self.level.is_end_level()

    def niveau_draw(self):
        if self.level.in_level:
            pyxel.cls(1)
            #Sol blanc
            pyxel.rect(0, self.cube.cube_y_min+16, self.screen_x, self.screen_y, 7)

            #Cube
            if self.cube.cube_rotation >= 0 and self.cube.cube_rotation < 10:
                pyxel.blt(self.cube.cube_x, self.cube.cube_y, 0, 0, 0, 16, 16, 0)
            elif self.cube.cube_rotation >= 10 and self.cube.cube_rotation < 40:
                pyxel.blt(self.cube.cube_x, self.cube.cube_y, 0, 16, 0, 16, 16, 0)
            elif self.cube.cube_rotation >= 40 and self.cube.cube_rotation < 50:
                pyxel.blt(self.cube.cube_x, self.cube.cube_y, 0, 32, 0, 16, 16, 0)
            elif self.cube.cube_rotation >= 50 and self.cube.cube_rotation <= 80:
                pyxel.blt(self.cube.cube_x, self.cube.cube_y, 0, 48, 0, 16, 16, 0)

            #Obstacles
            for obstacle in self.level.obstacle_liste:
                if obstacle['x'] < self.screen_x:
                    pyxel.blt(obstacle['x'], obstacle['y'], self.level.obstacles_pyxres[obstacle['type']]['image'], self.level.obstacles_pyxres[obstacle['type']]['x'], self.level.obstacles_pyxres[obstacle['type']]['y'], self.level.obstacles_pyxres[obstacle['type']]['width'], self.level.obstacles_pyxres[obstacle['type']]['height'], 0)

            if self.level.game_over:
                pyxel.text(70, 70, "GAME OVER", 8)
                pyxel.text(55, 80, "R pour recommencer", 7)

            if self.level.finish:
                pyxel.blt(self.screen_x//2-40, self.screen_y//2-20, 2, 0, 0, 64, 32 , 0) #Level complete
                pyxel.blt(100, 115, 1, 48, 0, 16, 16 , 0)   #Quitter
                pyxel.blt(170, 115, 1, 64, 0, 16, 16, 0) #Recommencer
            pyxel.text(self.screen_x//2-15, 5, f"{str(self.level.pourcentage)}%", 8)

            #ESC menu
            if self.level.ESC_level:
                pyxel.blt(5, 5, 1, 48, 0, 16, 16,0) #croix (quitter)
                pyxel.blt(self.screen_x/2-16, self.screen_y/2-16, 1, 0, 0, 32, 32,0) #bouton reprendre


    #Gamew
    def update(self):
        #Menu
        self.menu.menu_update()

        #Lvl editor
        self.level_editor.editor_update()

        #Cheats
        self.cheats.cheats_update()

        #Niveau en cours
        
        self.niveau_update()


    def draw(self):
        #menu
        self.menu.menu_draw()

        #Lvl editor
        self.level_editor.editor_draw()

        self.niveau_draw() #chaque level dessine la même chose

        #Cheats
        self.cheats.cheats_draw()

        



Game()