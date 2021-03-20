""" Module that manages buttons"""
from os import path
import pygame
from menucolors import Menu_colors


class Button:
    """
    A class to create, display and manage buttons

    Attributes
    ---------
    label : str
        text which will be displayed on the button
    x_pos, y_pos : float
        coordinates of the button on the screen
    width, height : float
        button's width and height
    color : Color
        button's inactive color
    action : str
        fonction that will be called when there will have a click on the button
    is_active : boolean
        inform if the button was clicked
    game_folder : str
            give the path of the current directory
    font_folder : str
        give the path to access to the "font" directory

    Methods
    -------
    draw(display : pygame.Surface)
        display the button on the screen
    activate(self)
        inform that the mouse is over the button which has to be displayed with its active color
    deactivate(self)
        inform that the mouse isn't over the button which has to be displayed
        with its inactive color
    set_status_on_mouse(pos: [int, int])
        allow to know if the mouse is over the button or not
    do_action(nom=None, classe=None, dic_abili=None, menu=None)
        allow to execute the fonction associated with the button
    """

    def __init__(self, label, x, y, w, h, action):
        """
        Parameters
        ---------
        label : str
            text which will be displayed on the button
        x_pos, y_pos : float
            coordinates of the button on the screen
        width, height : float
            button's width and height
        color : Color
            button's inactive color
        action : str
            fonction that will be called when there will have a click on the button
        is_active : boolean
            inform if the mouse is over the button
        """
        self.label = label
        self.x_pos = x
        self.y_pos = y
        self.width = w
        self.height = h
        self.color = pygame.Color("Peru")
        self.action = action
        self.is_active = False

        self.game_folder = path.dirname(__file__)
        self.font_folder = path.join(self.game_folder, "font")

    def draw(self, display: pygame.Surface):
        """display the button on the screen

        Parameters
        ----------
        display : Surface
            screen where the button has to be drawn
        """
        pygame.draw.rect(
            display, self.color, (self.x_pos, self.y_pos, self.width, self.height)
        )

        butt_text = pygame.font.Font(
            path.join(self.font_folder, "brushscriptitalique.ttf"), 30
        )
        butt_textsurf = butt_text.render(self.label, True, Menu_colors().black)
        butt_textrect = butt_textsurf.get_rect()
        butt_textrect.center = (
            (self.x_pos + (self.width / 2)),
            (self.y_pos + (self.height / 2)),
        )

        display.blit(butt_textsurf, butt_textrect)

    def activate(self):
        """inform that the mouse is over the button which
        has to be displayed with its active color"""

        self.is_active = True
        self.color = pygame.Color("Sienna")

    def deactivate(self):
        """inform that the mouse isn't over the button which
        has to be displayed with its inactive color"""

        self.is_active = False
        self.color = pygame.Color("Peru")

    def set_status_on_mouse(self, pos):
        """allow to know if the mouse is over the button or not

        Parameters
        ----------
        pos : [int, int]
            give the mouse's coordinates on the screen
        """

        if (
            self.x_pos <= pos[0] <= self.x_pos + self.width
            and self.y_pos <= pos[1] <= self.y_pos + self.height
        ):
            self.activate()
        else:
            self.deactivate()

    def do_action(
        self, nom=None, classe=None, portrayal=None, dic_abili=None, menu=None
    ):
        """allow to execute the fonction associated with the button

        Parameters
        ----------
        nom : str, optional
            character's name (default is None)
        classe : str, optional
            name of the character's class (default is None)
        dic_abili : dict, optional
            dictionary of the character's abilities (default is None)
        menu : __main__.creation_menu, optional
            allow to fill some menu's attributes in the called fonction
        """
        if (
            self.is_active
            and nom is None
            and classe is None
            and dic_abili is None
            and portrayal is None
        ):
            self.action()
        elif (
            self.is_active
            and nom is not None
            and classe is not None
            and dic_abili is not None
            and menu is not None
            and portrayal is not None
        ):
            self.action(nom, classe, portrayal, dic_abili, menu)
