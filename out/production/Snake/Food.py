import arcade
import Const


def Food(type, x, y):
    if type == 0:
        return _Food('images/apple.png', 0.2, type, x, y)
    elif type == 1:
        return _Food('images/speed.png', 0.2, type, x, y)
    elif type == 2:
        return _Food('images/slow.png', 0.2, type, x, y)
    elif type == 3:
        return _Food('images/ghost_walk.png', 0.2, type, x, y)
    else:
        return _Food('images/color.png', 0.2, type, x, y)


class _Food(arcade.Sprite):
    def __init__(self, image, scale, type, x, y):
        super().__init__(image, scale, center_x=x, center_y=y)
        self.type = type  # type of food - normal, speed, change_color, ghost walk etc
        self.setup()

    def setup(self):
        pass

    def get_position(self):
        return self.center_x, self.center_y

    def get_type(self):
        return self.type
