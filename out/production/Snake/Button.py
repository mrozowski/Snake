import arcade


class Button:
    """ Text-based button """

    def __init__(self, center_x, center_y, width, height, text, font_size=18, font_face="Arial"):
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.text = text
        self.font_size = font_size
        self.font_face = font_face
        self.pressed = False
        self.face_color = arcade.color.LIGHT_GRAY

    def draw(self):
        """ Draw the button """
        width = self.width
        height = self.height

        # Change size of button by 2px on press
        if self.pressed:
            width -= 2
            height -= 2

        arcade.draw_rectangle_filled(self.center_x, self.center_y, width, height, self.face_color)
        arcade.draw_text(self.text, self.center_x, self.center_y,
                         arcade.color.BLACK, font_size=self.font_size,
                         width=width, align="center",
                         anchor_x="center", anchor_y="center")

    def on_press(self):
        self.pressed = True

    def on_release(self):
        self.pressed = False

    def change_title(self, title):
        self.text = title

    def change_color(self, color):
        self.face_color = color


def check_mouse_press_for_buttons(x, y, button_list):
    """ Sprawdza czy mysz nadusiła ktoryś z przycisków. """
    for button in button_list:
        if x > button.center_x + button.width / 2:
            continue
        if x < button.center_x - button.width / 2:
            continue
        if y > button.center_y + button.height / 2:
            continue
        if y < button.center_y - button.height / 2:
            continue
        button.on_press()


def check_mouse_release_for_buttons(_x, _y, button_list):
    """ Jeżeli przycisk myszy został puszczony to sprawdż czy trzeba zmienić któryś z przycisków. """
    for button in button_list:
        if button.pressed:
            button.on_release()


class TextButton(Button):
    def __init__(self, title, center_x, center_y, width, height, size, action_function):
        super().__init__(center_x, center_y, width, height, title, size, "Arial")
        self.action_function = action_function

    def on_release(self):
        super().on_release()
        self.action_function()

    def change_title(self, new_title):
        super().change_title(new_title)

    def button_on(self, e):
        if e:
            self.change_color(arcade.color.LIGHT_GREEN)
        else:
            self.change_color(arcade.color.LIGHT_GRAY)

    def change_color(self, color):
        super().change_color(color)


class MenuButton(TextButton):
    def __init__(self, title, center_x, center_y, size, action_function):
        super().__init__(title, center_x, center_y, 120, 40, size, action_function)
        self.action_function = action_function


class SmallButton(TextButton):
    def __init__(self, title, center_x, center_y, size, action_function):
        super().__init__(title, center_x, center_y, 74, 30, size, action_function)
        self.action_function = action_function
