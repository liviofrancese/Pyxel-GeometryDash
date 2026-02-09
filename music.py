import pyxel

class Music:
    def __init__(self, game):
        self.game = game

    def resume_song(self):
        self.game.level.sec = 0
        for seconds in self.game.level.sec_list:
            self.game.level.sec += seconds
        if self.game.level.current_level == 'lvl1':
            pyxel.playm(1, sec=self.game.level.sec)
        if self.game.level.current_level == 'lvl2':
            pyxel.playm(2, sec=self.game.level.sec)
    def play_song(self):
        if self.game.level.current_level == 'lvl1':
            pyxel.playm(1)
        if self.game.level.current_level == 'lvl2':
            pyxel.playm(2)
    def stop_allsongs(self):
        pyxel.stop()
    def get_song_pos(self):
        self.game.level.music_position = pyxel.play_pos(0)
        if self.game.level.music_position is not None:
            self.game.level.sound, self.game.level.sec = self.game.level.music_position
            self.game.level.sec_list[self.game.level.sound] = self.game.level.sec
    def get_song_sec(self):
        self.game.level.sec_temp += self.game.level.sec
    def death_sound(self):
        if not self.game.level.death_sound_var:
            self.stop_allsongs()
            pyxel.play(0, 63)
            self.game.level.death_sound_var = True