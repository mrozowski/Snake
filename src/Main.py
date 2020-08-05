import arcade
from Button import SmallButton, check_mouse_press_for_buttons, check_mouse_release_for_buttons
import Const
from Rectangle import Rectangle
import random
import Body
import Food
import TimeReset
import Menu
import GhostWalk


def collision(_x, _y, x, y):
    if _x == x and _y == y:
        return True
    return False


class Snake(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height, title="Snake RunInto90s", fullscreen=True)
        arcade.set_background_color(arcade.color.BLACK)
        self.deaths = 0
        self.tail = 0
        self.best_score = 0
        self.level = 0
        self.button_list = []
        self.game_screen = None
        self.side_bar = None
        self.body = []
        self.tick = 0
        self.speed = 3  # 3 normal, 2 fast
        self.food = None
        self.point_bar = []
        self.is_menu = True
        self.menu = Menu.Menu(self)
        self.ghost_walk_indicator = None

    def setup(self):
        arcade.schedule(self.update, 1 / 30)
        (_w, _h) = arcade.get_window().get_size()

        w = int(_w / Const.BODY_SIZE) * Const.BODY_SIZE
        h = int(_h / Const.BODY_SIZE) * Const.BODY_SIZE
        Const.RIGHT = _w
        Const.TOP = Const.GAME_HEIGHT = h
        Const.SIDE_BAR = _w - w + Const.SIDE_BAR
        Const.GAME_WIDTH = _w - Const.SIDE_BAR
        Const.GRID_NR_W = int(Const.GAME_WIDTH / Const.BODY_SIZE)
        Const.GRID_NR_H = int(h / Const.BODY_SIZE)
        play_button = SmallButton('Menu', Const.RIGHT - Const.SIDE_BAR / 2, 200, 15, self.play_method)
        quit_button = SmallButton('Quit', Const.RIGHT - Const.SIDE_BAR / 2, 165, 15, self.quit_method)

        self.side_bar = Rectangle(_w - Const.SIDE_BAR, 0, Const.SIDE_BAR, Const.TOP, arcade.color.DARK_GRAY)
        self.button_list.append(play_button)
        self.button_list.append(quit_button)

        self.spawn_food()
        self.menu.setup()
        self.ghost_walk_indicator = GhostWalk.GhostWalkIndicator()

    def set_players(self, number_of_players):
        if number_of_players < 1:
            number_of_players = 1
        center_x = int(Const.GRID_NR_W / 2) * Const.BODY_SIZE + Const.BODY_SIZE / 2 + 2 * Const.BODY_SIZE
        center_y = int(Const.GRID_NR_H / 2) * Const.BODY_SIZE + Const.BODY_SIZE / 2
        p = 0
        self.body = []
        for i in range(number_of_players):
            player = Body.Body(i)
            player.set_position(center_x - p, center_y)
            player.setup()
            self.body.append(player)
            p += 4 * Const.BODY_SIZE

    def on_draw(self):
        arcade.start_render()

        self.side_bar.draw()
        for button in self.button_list:
            button.draw()
        if self.is_menu:
            self.menu.draw()
        else:
            arcade.draw_text("Points", Const.RIGHT - Const.SIDE_BAR / 2, Const.GAME_HEIGHT - 50, arcade.color.WHITE, 30,
                             align="center", anchor_x="center")
            y = Const.GAME_HEIGHT - 100
            for a in self.body:
                Body.Component(Const.RIGHT - Const.SIDE_BAR + 15, y + 20, a.size, a.color, a.kind).draw()
                arcade.draw_text(str(a.points), Const.RIGHT - Const.SIDE_BAR + 30, y, arcade.color.WHITE, 30,
                                 align="center", anchor_x="left")
                y -= 40

            for a in self.body:
                a.draw()

            if Const.GHOST_WALK:
                self.ghost_walk_indicator.draw()

            self.food.draw()

    def update(self, delta_time: float):
        if self.is_menu is False:
            for a in self.body:
                if self.tick % a.speed == 0:
                    # did they hit each other
                    for p in self.body:  # check collision with other snake
                        if a != p:
                            for segment in p.body:  # check all other snake segments position
                                if segment.x == a.x and segment.y == a.y:
                                    a.death()

                    (_x, _y) = self.food.get_position()

                    if collision(_x, _y, a.x, a.y):
                        # when eat food
                        type = self.food.get_type()
                        self.spawn_food()
                        a.eat()
                        a.points += 10

                        if type == 0:
                            a.points += 10
                            a.eat()  # eat again apple will give double points and 1 more segment
                        else:
                            if Const.SINGLE_PLAYER:
                                self.single_player_eat_process(a, type)
                            else:
                                self.multi_player_eat_process(a, type)

                    # if Const.DEATH:
                    #    #self.is_dead()

                    a.update()
                    # print(a.get_name())
            self.tick = self.tick + 1

    def single_player_eat_process(self, a, type):
        if type == 1:
            for p in self.body:  # change speed for other snakes
                self.change_state(a.timers, 0)
                a.speed -= 1
                if a.speed < 1: a.speed = 1
        elif type == 2:
            self.change_state(a.timers, 1)
            a.speed += 1  # slower
            if a.speed > 6: a.speed = 6
        elif type == 3:
            self.change_state(a.timers, 2)
            Const.GHOST_WALK = True
        elif type == 4:
            a.color = a.change_color()

    def multi_player_eat_process(self, a, type):
        if type == 1:
            for p in self.body:  # change speed for other snakes
                if a != p:
                    self.change_state(p.timers, 0)
                    p.speed -= 1
                    if p.speed < 1: p.speed = 1
        elif type == 2:
            for p in self.body:  # change speed for other snakes
                if a != p:
                    self.change_state(p.timers, 1)
                    p.speed += 1  # slower
                    if p.speed > 6: p.speed = 6
        elif type == 3:
            for p in self.body:
                self.change_state(p.timers, 2)
            Const.GHOST_WALK = True
        elif type == 4:
            for p in self.body:  # change color for other snakes
                if a != p:
                    p.color = p.change_color()

    def change_state(self, timer, index):
        # I could pass variable but apparently in python parameters like normal variable are passed by value
        # So I passed list to have parameter as reference
        if timer[index].is_alive():
            timer[index].reset()  # reset timer if was running already
        else:
            timer[index] = TimeReset.TimerReset(timer[index].interval, timer[index].function)
            timer[index].start()

    def spawn_food(self):
        x = int(random.random() * Const.GRID_NR_W) * Const.BODY_SIZE + Const.BODY_SIZE / 2
        y = int(random.random() * Const.GRID_NR_H) * Const.BODY_SIZE + Const.BODY_SIZE / 2
        type = int(random.random() * 5)
        # thank to this if normal apple (type 0) should appear 50% of the time
        if type != 0:
            type = int(random.random() * 5)

        self.food = Food.Food(type, x, y)

    def on_mouse_press(self, x, y, button, key_modifiers):
        check_mouse_press_for_buttons(x, y, self.button_list)
        check_mouse_press_for_buttons(x, y, self.menu.elements)

    def on_mouse_release(self, x, y, button, key_modifiers):
        check_mouse_release_for_buttons(x, y, self.button_list)
        check_mouse_release_for_buttons(x, y, self.menu.elements)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            if self.body[0].y_speed != -1:
                self.body[0].control(0, 1)
        elif key == arcade.key.LEFT:
            if self.body[0].x_speed != 1:
                self.body[0].control(-1, 0)
        elif key == arcade.key.RIGHT:
            if self.body[0].x_speed != -1:
                self.body[0].control(1, 0)
        elif key == arcade.key.DOWN:
            if self.body[0].y_speed != 1:
                self.body[0].control(0, -1)

        if len(self.body) > 1:
            if key == arcade.key.W:
                if self.body[1].y_speed != -1:
                    self.body[1].control(0, 1)
            elif key == arcade.key.A:
                if self.body[1].x_speed != 1:
                    self.body[1].control(-1, 0)
            elif key == arcade.key.D:
                if self.body[1].x_speed != -1:
                    self.body[1].control(1, 0)
            elif key == arcade.key.S:
                if self.body[1].y_speed != 1:
                    self.body[1].control(0, -1)

    def play_method(self):
        if len(self.body) > 0:
            if self.is_menu:
                self.button_list[0].change_title("Menu")
                self.is_menu = False
            else:
                self.button_list[0].change_title("Resume")
                self.is_menu = True

    def quit_method(self):
        exit(0)


def main():
    game = Snake(800, 600)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
