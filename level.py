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