import pyxel

class Cheats:
    def __init__(self, game):
        self.game = game

        self.noclip = False

    def noclip_change(self):
        if pyxel.btnp(pyxel.KEY_N):
            if self.noclip:
                return False
            return True
        else:
            return self.noclip

    def cheats_update(self):
        self.noclip = self.noclip_change()

    def cheats_draw(self):
        if self.noclip:
            pyxel.text(self.game.screen_x-30,5,"NOCLIP",8)