import arcade
import Const
from Button import MenuButton
from Food import Food


class Menu:
    def __init__(self, main):
        self.elements = []
        self.text_menu = None
        self.main = main
        self.center = 0
        self.high = 0
        """For instruction"""
        self.is_instruction = False
        self.icons = []

    def setup(self):
        self.is_instruction = False
        self.center = Const.GAME_WIDTH / 2
        self.high = Const.GAME_HEIGHT - Const.GAME_HEIGHT * 10 / 100
        self.text_menu = arcade.draw_text("Menu", self.center, self.high, arcade.color.WHITE, 30,
                                          align="center", anchor_x="center")
        single_player_button = MenuButton("Single player", self.center, self.high - 40, 15, self.single_player_mode)

        multi_players_button = MenuButton("2 players", self.center, self.high - 100, 15, self.multi_player_mode)
        instruction_button = MenuButton("Instruction", self.center, self.high - 160, 15, self.instruction)
        close_button = MenuButton("Close", self.center, self.high - 220, 15, self.close_method)

        self.elements.append(single_player_button)
        self.elements.append(multi_players_button)
        self.elements.append(instruction_button)
        self.elements.append(close_button)

    def draw(self):
        self.text_menu.draw()
        if self.is_instruction:
            for a in self.icons:
                a.draw()
            arcade.draw_text("Normal food that gives double points", self.center - 160, self.high-60, arcade.color.WHITE, 15, align="center", anchor_x="left")
            arcade.draw_text("Food that gives speed boost for 5 seconds to your opponent", self.center - 160, self.high-90, arcade.color.WHITE, 15, align="left", anchor_x="left")
            arcade.draw_text("Food that slow down your opponent for 5 seconds ", self.center - 160, self.high-120, arcade.color.WHITE, 15, align="left", anchor_x="left")
            arcade.draw_text("Eating this food enable walking through walls and through yourself for 5 seconds", self.center - 160, self.high-150, arcade.color.WHITE, 15, align="left", anchor_x="left")
            arcade.draw_text("Eating this food change color of your opponent", self.center - 160, self.high-180, arcade.color.WHITE, 15, align="left", anchor_x="left")

            arcade.draw_text("Keyboard - Player 1 use arrows keys to move", self.center , self.high-250, arcade.color.WHITE, 20, align="center", anchor_x="center")
            arcade.draw_text("Keyboard - Player 2 use WSAD keys to move", self.center , self.high-285, arcade.color.WHITE, 20, align="left", anchor_x="center")

        for a in self.elements:
            a.draw()

    def single_player_mode(self):
        Const.SINGLE_PLAYER = True
        Const.PLAYERS = 1
        self.main.set_players(1)
        self.main.is_menu = False

    def multi_player_mode(self):
        Const.SINGLE_PLAYER = False
        Const.PLAYERS = 2  # I made this field because maybe in future i'll try add more players and online mode
        self.main.set_players(2)
        self.main.is_menu = False

    def instruction(self):
        self.elements = []
        self.text_menu = arcade.draw_text("Instruction", self.center, self.high, arcade.color.WHITE, 30,
                                          align="center", anchor_x="center")

        icon_food = Food(0, self.center - 180, self.high - 50)
        icon_speed = Food(1, self.center - 180, self.high - 80)
        icon_slow = Food(2, self.center - 180, self.high - 110)
        icon_ghost_walk = Food(3, self.center - 180, self.high - 140)
        icon_color = Food(4, self.center - 180, self.high - 170)

        back_button = MenuButton("Close", self.center, self.high - 325, 15, self.setup)

        self.icons.append(icon_food)
        self.icons.append(icon_speed)
        self.icons.append(icon_slow)
        self.icons.append(icon_ghost_walk)
        self.icons.append(icon_color)

        self.elements.append(back_button)
        self.is_instruction = True

    def close_method(self):
        exit(0)
