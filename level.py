import pyxel
import json

class Level:
    def __init__(self, game):
        self.game = game

        #Phisique du jeu
        self.gravity = 1.12
        self.jump_strength = -8.15
        self.velocity_x = 4.4
        self.speed = self.velocity_x
        self.velocity_y = 0
        self.jump = False
        self.jump_status = False
        self.game_over = False

        #Obstacles
        self.pourcentage = 0
        self.obstacle_liste = []
        self.initialisation = False
        self.finish = False
        self.end = 0
        self.end_pourc = 0

        self.obstacles_pyxres = {
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
        self.collisions = {
            'cube': {
                'cube_gauche': self.game.cube.cube_x,
                'cube_droit': self.game.cube.cube_x+16,
                'cube_haut': self.game.cube.cube_y,
                'cube_bas': self.game.cube.cube_y+16
            },
            'spike': {
                'obs_gauche': 4,
                'obs_droit': 11,
                'obs_haut': 0,
                'obs_bas': 16
            },
            'turned spike': {
                'obs_gauche': 4,
                'obs_droit': 11,
                'obs_haut': 7,
                'obs_bas': 16
            },
            'block': {
                'obs_gauche': 0,
                'obs_droit': 16,
                'obs_haut': 0,
                'obs_bas': 16
            },
            'mur': {
                'obs_gauche': 0,
                'obs_droit': 16,
                'obs_haut': 0,
                'obs_bas': 16
            },
            'orb': {
                'obs_gauche': 0,
                'obs_droit': 16,
                'obs_haut': 0,
                'obs_bas': 16
            }
        }

        self.death_sound_var = False

        #Game
        self.in_level = False
        self.ESC_level = False
        self.current_level = None

        self.music_position = None
        self.sound = 0
        self.sec = 0
        self.sec_list = [0] * 64


    def reset_obstacles(self):
        self.obstacle_liste, self.end = self.get_json_data(self.game.levels[self.current_level]) #type: ignore


    def get_json_data(self, file):
        with open(file, 'r') as f:
            data = json.load(f)
            level_length = data['level_length']
            obstacle_liste = data['obstacles']
        return obstacle_liste, level_length
    

    def level_init(self):
        if not self.initialisation:
            pyxel.mouse(False)
            self.reset_obstacles()
            self.game.default_var()
            self.game.music.stop_allsongs()
            self.game.music.play_song()
            self.initialisation = True
    def jumping(self):
        self.jump = True
        self.velocity_y = self.jump_strength
        self.game.cube.cube_rot = True
    def deplacement_obstacles(self):
        for obstacle in self.obstacle_liste:
            obstacle['x'] -= self.speed
        for obstacle in self.obstacle_liste:
            if obstacle['x'] < -16:
                self.obstacle_liste.remove(obstacle)
    def obstacles_gestion(self):
        for obstacle in self.obstacle_liste:
            #Rester sur le bloc
            if obstacle['type']=='block' or obstacle['type']=='mur':
                cube_left = self.game.cube.cube_x
                cube_right = self.game.cube.cube_x + 16
                obs_left = obstacle['x']
                obs_right = obstacle['x'] + 16
                if (cube_right > obs_left and cube_left < obs_right and self.game.cube.cube_y + 16 <= obstacle['y'] and self.game.cube.cube_y + 16 + self.velocity_y >= obstacle['y']):
                    self.game.cube.cube_y = obstacle['y'] - 16
                    self.velocity_y = 0
                    self.jump = False

            #Utilisation de l'orb
            if obstacle['type']=='orb':
                if self.collision(obstacle) and pyxel.btn(pyxel.KEY_SPACE): #A CONTINUER
                    self.jumping()
                    obstacle['used']=True

            #Collisions
            if self.collision(obstacle) and not obstacle['type']=='orb' and self.cheats.noclip==False:
                self.game_over = True
                self.death_sound()
                self.stop()
                if pyxel.btnp(pyxel.KEY_R):
                    self.initialisation = False
    def collision(self, obstacle): #Utilisé dans obstacles_gestion()
        #obstacle hors écran
        if obstacle['x'] > self.game.screen_x:
            return False

        #Mise à jour de la position du cube
        self.collisions['cube'] = {
                'cube_gauche': self.game.cube.cube_x,
                'cube_droit': self.game.cube.cube_x+16,
                'cube_haut': self.game.cube.cube_y,
                'cube_bas': self.game.cube.cube_y+16
            }

        obs_gauche = obstacle['x']+self.collisions[obstacle['type']]['obs_gauche']
        obs_droit = obstacle['x']+self.collisions[obstacle['type']]['obs_droit']
        obs_haut = obstacle['y']+self.collisions[obstacle['type']]['obs_haut']
        obs_bas = obstacle['y']+self.collisions[obstacle['type']]['obs_bas']

        if (self.collisions['cube']['cube_droit'] > obs_gauche and self.collisions['cube']['cube_gauche'] < obs_droit and self.collisions['cube']['cube_bas'] > obs_haut and self.collisions['cube']['cube_haut'] < obs_bas):
            return True
        return False
    def cube_jump_rot(self):
        #Saut du cube
        if pyxel.btn(pyxel.KEY_SPACE) and self.jump==False:
            self.jumping()
        self.game.cube.cube_y += self.velocity_y
        self.velocity_y += self.gravity
        self.is_going_down()
        self.end -= self.speed

        if self.game.cube.cube_rot:
            self.game.cube.cube_rotation += 4
            if self.game.cube.cube_rotation >= 80:
                self.game.cube.cube_rotation = 0
        if self.jump==False:
            self.game.cube.cube_rotation = 0
            self.game.cube.cube_rot = False

        #Cube va au minimum au sol
        if self.game.cube.cube_y >= self.game.cube.cube_y_min:
            self.game.cube.cube_y = self.game.cube.cube_y_min
            self.jump = False
            self.velocity_y = 0
    def is_going_down(self):
        if not self.game.cube.going_down:
            self.game.cube.cube_y_before = self.game.cube.cube_y
            self.game.cube.going_down = True
        elif self.game.cube.going_down:
            self.game.cube.cube_y_now = self.game.cube.cube_y
            self.game.cube.going_down = False
            if self.game.cube.cube_y_before < self.game.cube.cube_y_now:
                self.jump = True
    def level_pourc(self):
        self.game.cube.cube_x_pourc += self.speed
        self.pourcentage = int(self.game.cube.cube_x_pourc/(self.end_pourc-self.game.cube.cube_x)*10000)
        self.pourcentage = self.pourcentage/100
        if self.pourcentage >= 100:
            self.pourcentage = 100
    def is_end_level(self):
        if self.game.cube.cube_x>=self.end:
            self.finish = True
        if self.finish:
            pyxel.mouse(True)
            self.stop()
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < 100+16 and pyxel.mouse_x > 100 and pyxel.mouse_y < 115+16 and pyxel.mouse_y > 115 or pyxel.btnp(pyxel.KEY_ESCAPE):
                self.QUIT_LEVEL()
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < 170+16 and pyxel.mouse_x > 170 and pyxel.mouse_y < 115+16 and pyxel.mouse_y > 115 or pyxel.btnp(pyxel.KEY_R):
                #pyxel.blt(170, 115, 1, 64, 0, 16, 16, 0) #Recommencer
                self.initialisation = False
    def stop(self):
        self.speed = 0
        self.velocity_y = 0
        self.jump = True
        self.game.cube.cube_rot = False
    def QUIT_LEVEL(self):
        self.reset_obstacles()
        self.game.music.stop_allsongs()
        self.game.default_var()
        #game
        self.in_level = False
        self.game.menu.in_menu = True
        self.game.menu.game_menu = 2
    def ESC(self):
        if self.ESC_level:
            pyxel.mouse(True)
            self.game.music.stop_allsongs()
            self.speed = 0
            self.velocity_y = 0
            self.jump = True
            self.game.cube.cube_rot = False
            #comment mettre la musique en pause ?

            #Quitter le niveau
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < 5+16 and pyxel.mouse_x > 5 and pyxel.mouse_y < 5+16 and pyxel.mouse_y > 5 or pyxel.btnp(pyxel.KEY_ESCAPE):
                self.QUIT_LEVEL()

            #Reprendre le niveau
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < self.game.screen_x/2+16 and pyxel.mouse_x > self.game.screen_x/2-16 and pyxel.mouse_y < self.game.screen_y/2+16 and pyxel.mouse_y > self.game.screen_y/2-16:
                self.game.music.resume_song()
                self.speed = self.velocity_x
                self.jump = self.jump_status
                self.jump_status = False
                pyxel.mouse(False)
                self.ESC_level = False

        if self.in_level and pyxel.btnp(pyxel.KEY_ESCAPE):
            self.jump_status = self.jump
            self.ESC_level = True