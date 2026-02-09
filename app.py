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

        self.level.niveau_draw() #chaque level dessine la même chose

        #Cheats
        self.cheats.cheats_draw()

        



Game()