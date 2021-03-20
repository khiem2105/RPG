"""Module that manages the buttons and the input box"""
import pygame


class Input:
    """
    A class used to represent an Input box

     ...

    Attributes
    ----------
    x : int
        x position of the input box
    y : int
        y position of the input box
    size : tuple(int, int)
        size of the input box. size is a tuple containing the width and height of the input box.
    name : str
        name is a positional argument that represent the name of the input box.
         It is mostly used in the map editor. (default = "")
    text : str
        text is a positional argument that is used to add a text
        in the input box at his creation. (default = "")

    Methods
    -------
    event(event, shortcut=False)
        Check if the mouse is colliding with the box.
        If the mouse is colliding and a boutton is pressed the user can type in the box.
        Depending of the state the input box does not add the key in the same maner.

    draw(screen, color=(0, 0, 0), shortcut=False)
        draw the input box : it name, it text and it rect

    """

    def __init__(self, x: int, y: int, size, name="", text=""):
        self.rect = pygame.Rect(x, y, *size)
        self.color = pygame.Color(0, 0, 0)
        self.text = text
        self.iscolliding = False
        self.name = name
        self.name_surface = pygame.font.SysFont("Cascadia code", 32).render(
            self.name, True, pygame.Color(0, 0, 0)
        )
        self.text_surface = pygame.font.SysFont("Cascadia code", 32).render(
            self.text, True, pygame.Color(0, 0, 0)
        )
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.x = x + self.rect.width // 2 - self.text_rect.width // 2
        self.istyping = False

    def event(self, event, shortcut=False):
        """event method that manages the user interaction
        with the input box"""
        try:
            self.iscolliding = self.rect.collidepoint(event.pos)
        except AttributeError:
            pass
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.istyping = not self.istyping
                if not shortcut:
                    self.text = ""
            else:
                self.istyping = False
            self.color = (
                pygame.Color(255, 212, 129) if self.istyping else pygame.Color(0, 0, 0)
            )
        if event.type == pygame.KEYDOWN:
            if self.istyping:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif not shortcut:
                    self.text += event.unicode
                else:
                    self.text = pygame.key.name(event.key)
                self.text_surface = pygame.font.SysFont("Cascadia code", 32).render(
                    self.text, True, pygame.Color(0, 0, 0)
                )

    def draw(self, screen, color=(0, 0, 0), shortcut=False):
        """method that draw the input box.
        It needs to be call at each frame."""
        self.name_surface = pygame.font.SysFont("Cascadia code", 32).render(
            self.name, True, pygame.Color(*color)
        )
        self.text_surface = pygame.font.SysFont("Cascadia code", 32).render(
            self.text, True, pygame.Color(*color)
        )
        screen.blit(self.name_surface, (self.rect.x + 5, self.rect.y - 25))
        if shortcut:
            pygame.draw.rect(screen, (90, 0, 0), self.rect)
        else:
            pygame.draw.rect(screen, color, self.rect, 5)
        if self.iscolliding or self.istyping:
            pygame.draw.rect(screen, (215, 154, 16), self.rect, 2)
        screen.blit(self.text_surface, (self.rect.x + 5, self.rect.y + 5))


class Button:
    """Class that manage button object
    and contains just a function to know if
    the user click on the button"""

    def __init__(self, x, y, size, name="", color=(0, 0, 0), ennemy=None):
        self.rect = pygame.Rect(x, y, *size)
        self.color = pygame.Color(0, 0, 0)
        self.text = name
        self.ennemy = ennemy
        self.iscolliding = False
        self.name_surface = pygame.font.SysFont("Cascadia code", 32).render(
            self.text, True, pygame.Color(*color)
        )
        self.text_rect = self.name_surface.get_rect()
        self.text_rect.x = x + self.rect.width // 2 - self.text_rect.width // 2

    def is_cliked(self, event):
        """fonction a part pour le bouton load savoir si il est cliqué"""
        try:
            self.iscolliding = self.rect.collidepoint(event.pos)
        except AttributeError:
            pass
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(event.pos)
