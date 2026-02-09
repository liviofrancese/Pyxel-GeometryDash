import pyxel
import json
import os
from editlvls import LevelEditor
from menu import Menu
from cube import Cube
from cheats import Cheats
from level import Level


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

#Songs
    def resume_song(self):
        self.level.sec = 0
        for seconds in self.level.sec_list:
            self.level.sec += seconds
        if self.level.current_level == 'lvl1':
            pyxel.playm(1, sec=self.level.sec)
        if self.level.current_level == 'lvl2':
            pyxel.playm(2, sec=self.level.sec)
    def play_song(self):
        if self.level.current_level == 'lvl1':
            pyxel.playm(1)
        if self.level.current_level == 'lvl2':
            pyxel.playm(2)
    def stop_allsongs(self):
        pyxel.stop()
    def get_song_pos(self):
        self.level.music_position = pyxel.play_pos(0)
        if self.level.music_position is not None:
            self.level.sound, self.level.sec = self.level.music_position
            self.level.sec_list[self.level.sound] = self.level.sec
    def get_song_sec(self):
        self.level.sec_temp += self.level.sec
    def death_sound(self):
        if not self.level.death_sound_var:
            self.stop_allsongs()
            pyxel.play(0, 63)
            self.level.death_sound_var = True


#level


    def level_init(self):
        if not self.level.initialisation:
            pyxel.mouse(False)
            self.level.reset_obstacles()
            self.default_var()
            self.stop_allsongs()
            self.play_song()
            self.level.initialisation = True
    def jumping(self):
        self.level.jump = True
        self.level.velocity_y = self.level.jump_strength
        self.cube.cube_rot = True
    def deplacement_obstacles(self):
        for obstacle in self.level.obstacle_liste:
            obstacle['x'] -= self.level.speed
        for obstacle in self.level.obstacle_liste:
            if obstacle['x'] < -16:
                self.level.obstacle_liste.remove(obstacle)
    def obstacles_gestion(self):
        for obstacle in self.level.obstacle_liste:
            #Rester sur le bloc
            if obstacle['type']=='block' or obstacle['type']=='mur':
                cube_left = self.cube.cube_x
                cube_right = self.cube.cube_x + 16
                obs_left = obstacle['x']
                obs_right = obstacle['x'] + 16
                if (cube_right > obs_left and cube_left < obs_right and self.cube.cube_y + 16 <= obstacle['y'] and self.cube.cube_y + 16 + self.level.velocity_y >= obstacle['y']):
                    self.cube.cube_y = obstacle['y'] - 16
                    self.level.velocity_y = 0
                    self.level.jump = False

            #Utilisation de l'orb
            if obstacle['type']=='orb':
                if self.collision(obstacle) and pyxel.btn(pyxel.KEY_SPACE): #A CONTINUER
                    self.jumping()
                    obstacle['used']=True

            #Collisions
            if self.collision(obstacle) and not obstacle['type']=='orb' and self.cheats.noclip==False:
                self.level.game_over = True
                self.death_sound()
                self.stop()
                if pyxel.btnp(pyxel.KEY_R):
                    self.level.initialisation = False
    def collision(self, obstacle): #Utilisé dans obstacles_gestion()
        #obstacle hors écran
        if obstacle['x'] > self.screen_x:
            return False

        #Mise à jour de la position du cube
        self.level.collisions['cube'] = {
                'cube_gauche': self.cube.cube_x,
                'cube_droit': self.cube.cube_x+16,
                'cube_haut': self.cube.cube_y,
                'cube_bas': self.cube.cube_y+16
            }

        obs_gauche = obstacle['x']+self.level.collisions[obstacle['type']]['obs_gauche']
        obs_droit = obstacle['x']+self.level.collisions[obstacle['type']]['obs_droit']
        obs_haut = obstacle['y']+self.level.collisions[obstacle['type']]['obs_haut']
        obs_bas = obstacle['y']+self.level.collisions[obstacle['type']]['obs_bas']

        if (self.level.collisions['cube']['cube_droit'] > obs_gauche and self.level.collisions['cube']['cube_gauche'] < obs_droit and self.level.collisions['cube']['cube_bas'] > obs_haut and self.level.collisions['cube']['cube_haut'] < obs_bas):
            return True
        return False
    def cube_jump_rot(self):
        #Saut du cube
        if pyxel.btn(pyxel.KEY_SPACE) and self.level.jump==False:
            self.jumping()
        self.cube.cube_y += self.level.velocity_y
        self.level.velocity_y += self.level.gravity
        self.is_going_down()
        self.level.end -= self.level.speed

        if self.cube.cube_rot:
            self.cube.cube_rotation += 4
            if self.cube.cube_rotation >= 80:
                self.cube.cube_rotation = 0
        if self.level.jump==False:
            self.cube.cube_rotation = 0
            self.cube.cube_rot = False

        #Cube va au minimum au sol
        if self.cube.cube_y >= self.cube.cube_y_min:
            self.cube.cube_y = self.cube.cube_y_min
            self.level.jump = False
            self.level.velocity_y = 0
    def is_going_down(self):
        if not self.cube.going_down:
            self.cube.cube_y_before = self.cube.cube_y
            self.cube.going_down = True
        elif self.cube.going_down:
            self.cube.cube_y_now = self.cube.cube_y
            self.cube.going_down = False
            if self.cube.cube_y_before < self.cube.cube_y_now:
                self.level.jump = True
    def level_pourc(self):
        self.cube.cube_x_pourc += self.level.speed
        self.level.pourcentage = int(self.cube.cube_x_pourc/(self.level.end_pourc-self.cube.cube_x)*10000)
        self.level.pourcentage = self.level.pourcentage/100
        if self.level.pourcentage >= 100:
            self.level.pourcentage = 100
    def is_end_level(self):
        if self.cube.cube_x>=self.level.end:
            self.level.finish = True
        if self.level.finish:
            pyxel.mouse(True)
            self.stop()
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < 100+16 and pyxel.mouse_x > 100 and pyxel.mouse_y < 115+16 and pyxel.mouse_y > 115 or pyxel.btnp(pyxel.KEY_ESCAPE):
                self.QUIT_LEVEL()
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < 170+16 and pyxel.mouse_x > 170 and pyxel.mouse_y < 115+16 and pyxel.mouse_y > 115 or pyxel.btnp(pyxel.KEY_R):
                #pyxel.blt(170, 115, 1, 64, 0, 16, 16, 0) #Recommencer
                self.level.initialisation = False
    def stop(self):
        self.level.speed = 0
        self.level.velocity_y = 0
        self.level.jump = True
        self.cube.cube_rot = False
    def QUIT_LEVEL(self):
        self.level.reset_obstacles()
        self.stop_allsongs()
        self.default_var()
        #game
        self.level.in_level = False
        self.menu.in_menu = True
        self.menu.game_menu = 2
    def ESC(self):
        if self.level.ESC_level:
            pyxel.mouse(True)
            self.stop_allsongs()
            self.level.speed = 0
            self.level.velocity_y = 0
            self.level.jump = True
            self.cube.cube_rot = False
            #comment mettre la musique en pause ?

            #Quitter le niveau
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < 5+16 and pyxel.mouse_x > 5 and pyxel.mouse_y < 5+16 and pyxel.mouse_y > 5 or pyxel.btnp(pyxel.KEY_ESCAPE):
                self.QUIT_LEVEL()

            #Reprendre le niveau
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < self.screen_x/2+16 and pyxel.mouse_x > self.screen_x/2-16 and pyxel.mouse_y < self.screen_y/2+16 and pyxel.mouse_y > self.screen_y/2-16:
                self.resume_song()
                self.level.speed = self.level.velocity_x
                self.level.jump = self.level.jump_status
                self.level.jump_status = False
                pyxel.mouse(False)
                self.level.ESC_level = False

        if self.level.in_level and pyxel.btnp(pyxel.KEY_ESCAPE):
            self.level.jump_status = self.level.jump
            self.level.ESC_level = True




    #level update et draw
    def niveau_update(self):
        if self.level.in_level:
            #Level initialization
            self.level_init()

            #Get song position
            self.get_song_pos()

            #Gestion d'obstacles
            self.obstacles_gestion()

            #Obstacles:
            self.deplacement_obstacles()

            #Pourcentage du niveau:
            self.level_pourc()

            #Gestion du cube
            self.cube_jump_rot()

            #ESC
            self.ESC()

            #endlevel
            self.is_end_level()

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