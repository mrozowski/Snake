import arcade
import Const


class GhostWalkEffect:
    def __init__(self):
        self.show = True
        self.shape = arcade.draw_rectangle_outline(Const.GAME_WIDTH/2, Const.GAME_HEIGHT/2, Const.GAME_WIDTH -1, Const.GAME_HEIGHT-2, (70, 127, 183), 3)

    def draw(self):
        self.shape.draw()

