from copy import deepcopy

import arcade
import Const
import TimeReset
import random

class Body:
    def __init__(self, kind):
        self.size = 20
        self.x = 0
        self.y = 0
        self.x_speed = 0
        self.y_speed = 0
        self.length = 0
        self.points = 0
        self.body = []
        self.speed = 3
        self.color = None
        self.name = "Snake"
        self.timers = []
        self.default_x = 0
        self.default_y = 0
        self.default_color = arcade.color.WHITE
        self.kind = kind

    def setup(self):
        self.timers.append(TimeReset.TimerReset(Const.INTERVAL, self.normal_speed))
        self.timers.append(TimeReset.TimerReset(Const.INTERVAL, self.normal_speed))
        self.timers.append(TimeReset.TimerReset(Const.INTERVAL, self.normal_walk))
        #self.random_position()
        self.default_color = self.change_color()
        self.color = self.default_color
        self.set_player()


    def set_position(self, x, y):
        self.default_x = x
        self.default_y = y

    # def random_position(self):
    #     self.default_x = int(random.random() * Const.GRID_NR_W) * Const.BODY_SIZE + Const.BODY_SIZE / 2
    #     self.default_y = int(random.random() * Const.GRID_NR_H) * Const.BODY_SIZE + Const.BODY_SIZE / 2
    #     self.x = self.default_x
    #     self.y = self.default_y

    def set_player(self):
        self.length = 0
        self.points = 0
        self.x = self.default_x
        self.y = self.default_y
        self.body = []
        head = Component(self.x, self.y, self.size, self.color, self.kind)
        self.body.append(head)

    def update(self):
        self.body.pop(0)
        # make a move
        self.x = self.x + self.x_speed * self.size
        self.y = self.y + self.y_speed * self.size
        if Const.GHOST_WALK is False:
            self.check_collision()
        else:
            self.x = self.x % Const.GAME_WIDTH
            self.y = self.y % Const.GAME_HEIGHT

        head = Component(self.x, self.y, self.size, self.color, self.kind)
        self.body.append(head)

    def check_collision(self):
        # check collision with walls
        if self.x < 0 or self.x > Const.GAME_WIDTH or self.y < 0 or self.y > Const.GAME_HEIGHT:
            self.death()
        for a in self.body:
            if self.x == a.x and self.y == a.y:
                self.death()

    def death(self):
        self.set_player()
        self.color = self.default_color
        for a in self.timers:
            a.terminate()

        Const.DEATH = True

    def normal_walk(self):
        Const.GHOST_WALK = False

    def normal_speed(self):
        self.speed = 3

    def eat(self):
        self.length += 1
        self.body.append(Component(self.x, self.y, self.size, self.color, self.kind))

    def control(self, x, y):
        self.x_speed = x
        self.y_speed = y

    def draw(self):
        for a in self.body:
            a.draw()

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def change_color(self):
        r = random.uniform(0, 255)
        g = random.uniform(0, 255)
        b = random.uniform(0, 255)
        return r, g, b

class Component:
    def __init__(self, x, y, size,color, kind):
        self.x = x
        self.y = y
        self.kind = kind
        if self.kind == 0:
            self.shape = arcade.create_rectangle_filled(self.x, self.y, size, size, color)
        else:
            self.shape = arcade.create_ellipse_filled(self.x, self.y, size / 2, size / 2, color)


    def draw(self):
        self.shape.draw()
