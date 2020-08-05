import arcade
import Const


class GhostWalkIndicator:
    def __init__(self):
        self.show = 0
        self.shape = arcade.create_rectangle_outline(Const.GAME_WIDTH/2, Const.GAME_HEIGHT/2, Const.GAME_WIDTH -1, Const.GAME_HEIGHT-2, (70, 127, 183), 3)

    def draw(self):
        if self.show < 12:
            self.shape.draw()
        self.show += 1
        self.show %= 24




