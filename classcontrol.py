"""Module that contains Class_control"""
from os import path
import pygame
from button import Button
from menucolors import Menu_colors


class ClassControl:
    """
    A class used to display the buttons to control the choice/selection
    of character's class and display the current class

    Attributes
    ----------
    next_class : Button
        display the "next" button which allow to go to the next class
    previous_class : Button
        display the "previous" button which allow to go to the previous class
    x, y : float
        coordinates where the button has to be displayed
    game_folder : str
            give the path of the current directory
    font_folder : str
        give the path to access to the "font" directory

    Methods
    -------
    draw(display : pygame.Surface, class_name)
        display the next and previous button and the name of the current choosen class
    aff_text(size, X, Y, classe_name, display : pygame.Surface)
        allow to display the current choosen class with a specific size on a screen
        according to the X and Y coordinates
    get_buttons()
        return the "next" and "previous" buttons
    """

    def __init__(self, x, y, off, next_func, prev_func):
        """
        Parameters
        ----------
        next_class : Button
            display the "next" button which allow to go to the next class
        previous_class : Button
            display the "previous" button which allow to go to the previous class
        x, y : float
            coordinates where the button has to be displayed
        """
        self.next_class = Button("Next", x + off, y, 100, 50, next_func)
        self.previous_class = Button("Previous", x, y, 100, 50, prev_func)
        self.x_pos = x
        self.y_pos = y

        self.game_folder = path.dirname(__file__)
        self.font_folder = path.join(self.game_folder, "font")

    def draw(self, display: pygame.Surface, class_name):
        """display the next and previous button and the name of the current choosen class

        Parameters
        ----------
        display : Surface
            screen where the text has to be displayed
        class_name : str
            name of the current choosen class
        """
        offset_x_bouton = 225
        offset_y_bouton = 25
        size = 30
        self.next_class.draw(display)
        self.previous_class.draw(display)
        self.aff_text(
            size,
            self.x_pos + offset_x_bouton,
            self.y_pos + offset_y_bouton,
            class_name,
            display,
        )

    def aff_text(self, size, xpos, ypos, classe_name, display: pygame.Surface):
        """allow to display the current choosen class with a specific size
        on a screen according to the X and Y coordinates

        Parameters
        ----------
        size : int
            size of the text on the screen
        X, Y : float
            coordinates where the text has to be displayed
        classe_name : str
            the name of the current choosen class which will be displayed on the screen
        display : Surface
            screen where the text has to be displayed
        """

        butt_text = pygame.font.Font(
            path.join(self.font_folder, "brushscriptitalique.ttf"), size
        )
        butt_textsurf = butt_text.render(
            "Your class : " + classe_name, True, Menu_colors().black
        )
        butt_textrect = butt_textsurf.get_rect()
        butt_textrect.center = (xpos, ypos)
        display.blit(butt_textsurf, butt_textrect)

    def get_buttons(self):
        """return the "next" and "previous" buttons"""
        return [self.next_class, self.previous_class]
