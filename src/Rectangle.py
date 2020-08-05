import arcade


class Rectangle:
    def __init__(self, x, y, width, height, color):
        self.x = x + int(width / 2)
        self.y = y + int(height / 2)
        self.width = width
        self.height = height
        self.color = color
        self.shape = arcade.create_rectangle_filled(self.x, self.y, self.width, self.height, self.color)


    def draw(self):
        self.shape.draw()

    def change_color(self, color):
        self.shape = arcade.create_rectangle_filled(self.x, self.y, self.width + 2, self.height + 1, color)
