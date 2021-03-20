"""A module used to display the buttons and values of the character's abilities"""
from os import path
import pygame
import menucolors as mc
import button


class AbilityControl:
    """
    A class used to display the buttons and values of the character's abilities

    Attributes
    ----------
    decrease : Button
        allow to decrease the value of the associated ability
    increase : Button
        allow to increase the value of the associated ability
    ability : str
        ability associted with the buttons
    x, y : float
        coordinates where the texts (and buttons) have to be displayed
    game_folder : str
            give the path of the current directory
    font_folder : str
        give the path to access to the "font" directory

    Methods
    -------
    aff_text(size, X, Y, score, display : pygame.Surface)
        allow to display the value of the ability with a specific size on a screen
        according to the X and Y coordinates
    draw(display : pygame.Surface, score)
        allow to display the button and value associated with the ability
    get_buttons()
        return the buttons associated with the ability to decrease and increase its value
    """

    def __init__(self, x, y, ability, offset, inc_function, dec_function):
        """
        Parameters
        ----------
        x, y : float
            coordinates where the texts (and buttons) have to be displayed
        ability : str
            ability associted with the buttons
        offset : float
            offset added to the x value to indicate the right place
            where the button has to be displayed
        inc_function : str
            indicate the function that will be called to increment the
            ability's value associted with the button
        dec_function : str
            indicate the function that will be called to decrement the
            ability's value associted with the button
        """
        self.decrease = button.Button("-", x, y, 100, 50, dec_function)
        self.increase = button.Button("+", x + offset, y, 100, 50, inc_function)
        self.ability = ability
        self.x_pos = x
        self.y_pos = y

        self.game_folder = path.dirname(__file__)
        self.font_folder = path.join(self.game_folder, "font")

    def aff_text(self, size, pos, score, display: pygame.Surface):
        """allow to display the value of the ability with a specific size
        on a screen according to the X and Y coordinates

        Parameters
        ----------
        size : int
            size of the text/score on the screen
        X, Y : float
            coordinates where the text/score has to be displayed
        score : int
            the value of the ability
        display : Surface
            screen where the text/score has to be displayed
        """

        butt_text = pygame.font.Font(
            path.join(self.font_folder, "brushscriptitalique.ttf"), size
        )
        butt_textsurf = butt_text.render(
            self.ability + ":" + str(score), True, mc.Menu_colors().black
        )
        butt_textrect = butt_textsurf.get_rect()
        butt_textrect.center = (pos[0], pos[1])
        display.blit(butt_textsurf, butt_textrect)

    def draw(self, display: pygame.Surface, score):
        """allow to display the button and value associated with the ability

        Parameters
        ----------
        display : Surface
            screen where the text/score has to be displayed
        score : int
            the value of the ability
        """

        offset_x_bouton = 225
        offset_y_bouton = 25
        size = 30
        self.decrease.draw(display)
        self.increase.draw(display)
        self.aff_text(
            size,
            (self.x_pos + offset_x_bouton, self.y_pos + offset_y_bouton),
            score,
            display,
        )

    def get_buttons(self):
        """return the buttons associated with the ability to decrease and increase its value"""
        return [self.increase, self.decrease]
