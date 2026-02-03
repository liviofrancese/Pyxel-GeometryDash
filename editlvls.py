import pyxel



class LevelEditor:
    def __init__(self, game):
        #init all variables
        self.game = game

        self.in_editor = False

    def editor_update(self):
        pass


    def editor_draw(self):
        pyxel.cls(1)