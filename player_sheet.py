import pygame
from os import path
from box import Button
import settings


class player_sheet:
    """
    A class used to display the full description of the character

    Attributes
    ----------
    display_width, display_height : float
        width and height of the game's window/screen
    screen : Surface
        the screen/window where the "game" is displayed
    isActive : boolean
        indicate if the window/sheet must be active/display
    initialised : boolean
        indicate if the portrayal has to be initialised or not
    dic_player : dict
        dictionary that contains all the caracteristics of the character
    portrayal : str, optional
        name of the image used for the portrayal (default is None)
    resize_portrayal : Surface
        the image's/portrayal's size reduced
    game_folder : str
        give the path of the current directory
    img_folder :
        give the path to access to the "img" directory
    font_folder : str
        give the path to access to the "font" directory
    background : Surface
        the surface where the menu's font image is displayed

    Methods
    -------
    open()
        allow to initialise the portrayal (with the good size) if the image has to be initialised,
        and to display the character's description if the description has to be active/displayed
    close()
        if the spacebar is pressed, the description will be closed
    draw()
        display the description on the screen
    Aff_text(msg, size, X, Y,display : pygame.Surface)
        allow to display the message with a specific size on a screen according to the X and Y coordinates
    resize()
        allow to shrink the size of the image used for the portrayal
    """

    def __init__(self, screen: pygame.Surface, dic_player=None, portrayal=None):
        """
        If the arguments "portrayal" and "dic_player" aren't passed in (and if the image is not initialized),
        the sheet won't be displayed correctly, the game will be closed

        Parameters
        ----------
        screen : Surface
            the screen/window where the "game" is displayed
        dic_player : dict, optional
            dictionary that contains all the caracteristics of the character
        portrayal : str, optional
            name of the image used for the portrayal (default is None)
        """
        (
            self.display_width,
            self.display_height,
        ) = pygame.display.get_surface().get_size()
        self.screen = screen
        self.isActive = True
        self.initialised = False
        self.dic_player = dic_player
        self.list_button = dict()
        self.portrayal = portrayal
        self.resize_portrayal = None
        self.game_folder = path.dirname(__file__)
        self.img_folder = path.join(self.game_folder, "img")
        self.font_folder = path.join(self.game_folder, "font")
        self.background = pygame.transform.scale(
            pygame.image.load(
                path.join(self.img_folder, "img_menu_rules___character_creation.png")
            ),
            (720, 360),
        )
        self.surf = None

    def open(self):
        """
        allow to initialise the portrayal (with the good size) if the image has to be initialised,
        and to display the character's description if the description has to be active/displayed

        """

        if self.initialised:
            self.resize()
        if not self.isActive:
            self.surf = None
            self.isActive = True
        elif self.isActive:
            self.surf = self.draw()
            self.isActive = False

    def close(self):
        """if the spacebar is pressed, the description will be closed"""
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.isActive = False

    def draw(self):
        """display the description on the screen"""
        surf = pygame.Surface((720, 360))
        surf.blit(self.background, (0, 0))

        offset_text_x = 200
        offset_text_y = 40
        offset_Y = 0
        offset_X = 0
        size = 30
        column_number = 1
        first_line = True
        for i, cara in enumerate(self.dic_player):

            if cara != "spells":
                _ = pygame.font.Font(
                    path.join(self.font_folder, "brushscriptitalique.ttf"), size).render(
                    cara + " : " + str(self.dic_player[cara]), True, settings.BLACK
                )
                if (
                    (2 <= i <= 7)
                    and self.dic_player["carac point"] != 0
                    and self.dic_player[cara] < 18
                ):
                    self.list_button[cara] = Button(
                        _.get_rect()[2]
                        + 20
                        + offset_text_x * offset_X
                        + settings.WIDTH // 2
                        - surf.get_rect().width // 2,
                        offset_text_y * offset_Y
                        - _.get_rect()[3] / 4
                        + settings.HEIGHT // 2
                        - surf.get_rect().height // 2,
                        (30, 30),
                        name="+",
                        color=settings.BLACK,
                        ennemy=None,
                    )
                    surf.blit(
                        self.list_button[cara].name_surface,
                        (
                            _.get_rect()[2] + 20 + offset_text_x * offset_X,
                            offset_text_y * offset_Y - _.get_rect()[3] / 4,
                        ),
                    )

                surf.blit(_, (10 + offset_text_x * offset_X, offset_text_y * offset_Y))

                if first_line:
                    if offset_X == 1:
                        offset_Y += 2
                        offset_X = 0
                        first_line = False
                    else:
                        offset_X += 1

                elif not first_line and column_number == 1:

                    if offset_Y < 7:
                        offset_Y += 1
                    else:
                        offset_Y = 3
                        offset_X += 1
                        column_number += 1
                else:
                    offset_Y += 1

        surf.blit(self.resize_portrayal, (500, 10))
        return surf

    def resize(self):
        """allow to shrink the size of the image used for the portrayal"""
        portrayal_img_folder = path.join(
            self.game_folder, "img\\" + "portrayal_bank\\" + self.dic_player["class"]
        )
        portrayal = pygame.image.load(path.join(portrayal_img_folder, self.portrayal))
        self.resize_portrayal = pygame.transform.rotozoom(portrayal, 0, 1 / 5.5)
        self.initialised = False
