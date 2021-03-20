"""Module that manage inputbox"""
import pygame
from menucolors import Menu_colors
from os import path


class InputBox:
    """
    A class used to make an input box

    Attributes
    ----------
    rect : Rect
        rectangle where the input box will be displayed
    color : Color
        color of the input box
    text_begining : boolean
        indicate if the text in the input box is the default text or not
    text : str
        text enter by the user
    game_folder : str
            give the path of the current directory
    font_folder : str
        give the path to access to the "font" directory
    font_InputBox : Font
        define the font size and font name
    txt_surface : Surface
        display the text
    active : boolean
        indicate if the input box was clicked

    Methods
    -------
    handle_event(event)
        define actions/modifications of the input box according to different user's actions
         (mouse's click or keyboard's buttons press)
    update()
        resize the box if the text is too long/short
    draw(screen : pygame.Surface)
        display the input box
    """

    def __init__(self, x, y, w, h, text=""):
        """
        Parameters
        ----------
        x, y : float
            coordinates where the input box has to be displayed
        w, h : float
            width and height of the input box
        text : str
            text displayed in the input box
        """
        self.rect = pygame.Rect(x, y, w, h)
        self.color = Menu_colors().color_inactive
        self.text_begining = True
        self.text = text

        self.game_folder = path.dirname(__file__)
        self.font_folder = path.join(self.game_folder, "font")
        self.font_inputbox = pygame.font.Font(
            path.join(self.font_folder, "brushscriptitalique.ttf"), 25
        )
        self.txt_surface = self.font_inputbox.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        """
        define actions/modifications of the input box according to different user's actions
         (mouse's click or keyboard's buttons press)

        Parameters
        ----------
        event : Eventlist
            list of the different events that occur on the screen
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = (
                Menu_colors().color_active
                if self.active
                else Menu_colors().color_inactive
            )
            if self.active and self.text_begining:
                self.text = ""
                self.txt_surface = self.font_inputbox.render(
                    self.text, True, self.color
                )
                self.text_begining=False
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                # give a limit to the text's lenght
                elif self.txt_surface.get_width() + 10 < 200:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.font_inputbox.render(
                    self.text, True, self.color
                )

    def update(self):
        """resize the box if the text is too long/short"""
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen: pygame.Surface):
        """display the input box

        Parameters
        ----------
        screen : Surface
            screen where the input box has to be displayed
        """
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)


# _____Inspiré du programme disponible sur stack overflow:
#  https://stackoverflow.com/questions/46390231/how-can-i-create-a-text-input-box-with-pygame/46390412#46390412
