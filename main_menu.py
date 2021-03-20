import pygame
from pygame import mixer
import pickle
from pygame.constants import RESIZABLE
import pygame_menu
from pygame_menu import sound
from datetime import datetime
from os import path, listdir


# WINDOW_SIZE = (1500, 850)
HELP = [
    "Comment jouer :",
    "lancer le script bach puis le fichier run.py",
    "Sur le menu aller dans news game/load game.",
    "En jeu :",
    "Clique droit pour se déplacer/attaquer un ennemie",
    "Clique gauche choisir la cible d'un sort une fois cast.",
    "Une console est disponible en faisant TAB avec les commandes suivantes :",
    "/set Str int",
    "/set Con int",
    "/set Int int",
    "/set Wis int",
    "/set Dex int",
    "/set Cha int",
    "/set level int",
    "/kill : tue les ennemies autour de soit",
    "/heal : rend toute la vie et le mana",
    "/give item int[1-43] : donne l'item de l'entier passer en paramètre",
    "Toutes les autres controles  se retrouvent dans l'onglet shortcut lorsqu'on fait échap en jeu",
    "Bon jeu à vous ! ",
]


# Classe de test pour chopper les images et thème de manière plus "propre"
""" Class for somes methodes not a real objet class

Get_picture() : return path of a picture in parameters
get_sound( : return path of a sound in parameters)
get_theme : return theme you can only choose img background or img for widgets
set_font(): return font

"""


def get_picture(picture_name, MODE):
    """
    return the patch of a png, and put wich mode it will be print on the screen

    :param picture: the picturname wich end with .png
    :type file_loc: string
    :MODE: How it will be prints
    :type print_cols: string (check pygame_menu doc)
    :return : myimage : path and how img is print

    """
    game_folder = path.dirname(__file__)
    img_folder = path.join(game_folder, "img")
    pic_paths = path.join(img_folder, picture_name)
    test = path.join(img_folder, pic_paths)
    mainpath = path.join(game_folder, test)

    myimage = pygame_menu.baseimage.BaseImage(
        image_path=mainpath,
        drawing_mode=MODE,
    )

    return myimage


def get_sound(sound_name):
    """
    return the patch of sound wich is in sound folder

    :param sound_name: soundname need to end with.mp3
    :type file_loc: string
    : return : mainpath : path of the sound
    """

    game_folder = path.dirname(__file__)
    img_folder = path.join(game_folder, "sound")
    pic_paths = path.join(img_folder, sound_name)
    test = path.join(img_folder, pic_paths)
    mainpath = path.join(game_folder, test)

    return mainpath


def set_font(font_name):

    return pygame.font.match_font(font_name)


def get_theme(widget_img, background_img):
    """
    Used for set the background_img and the widget_img for all our themes

    :param widget_img : Widget name, must be in png or jpg
    :type : string
    :param background_img : background name, must be in png or jpg
    :type : string
    :return theme : theme used for menus
    """

    theme = pygame_menu.themes.Theme(
        cursor_color=(111, 82, 23),
        focus_background_color=(111, 82, 23, 200),
        background_color=get_picture(
            background_img, pygame_menu.baseimage.IMAGE_MODE_FILL
        ),  # transparent background
        title_shadow=True,
        title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_UNDERLINE_TITLE,
        title_font=set_font("brushscript"),
        title_font_size=75,
        title_shadow_color=(111, 82, 24),
        widget_background_color=get_picture(
            widget_img, pygame_menu.baseimage.IMAGE_MODE_FILL
        ),
        widget_alignment=pygame_menu.locals.ALIGN_CENTER,
        widget_font=set_font("brushscript"),
        widget_margin=(10, 15),
        widget_shadow=True,
    )

    return theme


# IN PROGRESS WILL BE DONE BEFORE 13/10/2020
class MainMenu:
    """Create object main menu"""

    def __init__(self):
        pygame.init()

        self.surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.my_font = set_font("brushscript")
        self.main_theme = get_theme("plank.png", "dungeon.jpg")
        self.engine = None
        self.sounds()

        self.menu = pygame_menu.Menu(
            center_content=True,
            height=self.surface.get_height(),  # Fullscreen
            onclose=pygame_menu.events.EXIT,  # Pressing ESC button does nothing
            theme=self.main_theme,
            title="Dungeon and Diablo",
            width=self.surface.get_width(),
        )

        self.is_started = False
        self.path_ = path.dirname(__file__) + "/save/"
        self.map_path_ = path.dirname(__file__) + "/map/"
        self.save_name = "default_save"
        self.name = None
        self.selected_save = None
        self.isload = False
        self.state = None

    def sounds(self):
        """Set the sound of menu and the sound effect when we change fo widget"""
        pygame.mixer.music.load(get_sound("tavern_sound.mp3"))
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(0.025)

        self.engine = sound.Sound(uniquechannel=False, frequency=10)
        self.engine.set_sound(
            sound.SOUND_TYPE_WIDGET_SELECTION, get_sound("menu_select.mp3"), volume=0.1
        )

    def add_widget(self):
        """fonction to add all widget we need to our menu"""
        self.menu.add_button("Play", self.start_the_game())
        self.menu.add_button("Rules", self.rules())
        self.menu.set_sound(self.sounds(), recursive=True)

        self.menu.add_button("Quit", pygame_menu.events.EXIT)

    def update(self):
        """update function"""
        print("is play starter", self.is_started)
        while self.state != "New Game" and not self.isload:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()

            if self.menu.is_enabled():
                self.menu.update(events)
                self.menu.draw(self.surface)

            pygame.display.update()

    def start_the_game(self):
        """
        Create and return the play_menu
        """

        self.play_theme = get_theme("plank.png", "play_menu.png")

        self.play_menu = pygame_menu.Menu(
            height=self.surface.get_height(),
            onclose=pygame_menu.events.DISABLE_CLOSE,
            theme=self.play_theme,
            title="Play",
            width=self.surface.get_width(),
        )

        self.play_menu.add_button("New Game", self.New_Game())
        self.play_menu.add_button("Load Game", self.Load_Game())

        return self.play_menu

    def settings(self):
        """
        Create and return the setting menu
        """

        setting_theme = get_theme("plank.png", "setting_menu.jpg")

        setting_menu = pygame_menu.Menu(
            height=self.surface.get_height(),
            rows=4,
            columns=3,
            onclose=pygame_menu.events.DISABLE_CLOSE,
            theme=setting_theme,
            title="Settings",
            width=self.surface.get_width(),
        )

        for i in range(12):
            setting_menu.add_button(i, None)

        return setting_menu

    def rules(self):
        """
        create and return rules Menu
        """

        help_theme = pygame_menu.themes.Theme(
            background_color=(
                get_picture("menu_rules.png", pygame_menu.baseimage.IMAGE_MODE_FILL)
            ),  # transparent background
            focus_background_color=(125, 91, 45, 125),
            title_shadow=True,
            title_background_color=(100, 100, 126),
            title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_UNDERLINE_TITLE,
            title_font=set_font("brushscript"),
            title_font_size=75,
            title_shadow_color=(111, 82, 24),
            widget_alignment=pygame_menu.locals.ALIGN_CENTER,
            widget_selection_effect=pygame_menu.widgets.NoneSelection(),
            widget_font=set_font("brushscript"),
        )

        help_menu = pygame_menu.Menu(
            height=self.surface.get_height(),  # Fullscreen
            onclose=pygame_menu.events.DISABLE_CLOSE,  # Pressing ESC button does nothing
            theme=help_theme,
            title="Help",
            width=self.surface.get_width(),
            menu_position=(1, 50),
            mouse_motion_selection=True,
        )
        for m in HELP:
            help_menu.add_label(m, align=pygame_menu.locals.ALIGN_CENTER)
        help_menu.add_vertical_margin(25)
        help_menu.add_button("Return to Menu", pygame_menu.events.BACK)

        return help_menu

    def New_Game(self):
        """ lauche the game  """
        play_theme = get_theme("plank.png", "play_menu.png")

        play_menu = pygame_menu.Menu(
            height=self.surface.get_height(),
            onclose=pygame_menu.events.DISABLE_CLOSE,
            theme=play_theme,
            title="Load game",
            width=self.surface.get_width(),
        )

        play_menu.add_text_input(
            "Save name :", default="default", onchange=self.check_name, maxwidth=32
        )

        for i in listdir(self.map_path_):
            play_menu.add_button(i, self.start, i)

        self.is_started = True
        print("dans new game", self.is_started)
        return play_menu

    def check_name(self, value):
        print("User name:", value)
        self.save_name = value

    def start(self, save_name):
        pygame.mixer.music.unload()
        self.name = save_name
        self.state = "New Game"

    def Load_Game(self):
        """
        create and return Load game Menu, save1,save2,save3 will be use for save slot
        """
        play_theme = get_theme("plank.png", "play_menu.png")

        play_menu = pygame_menu.Menu(
            height=self.surface.get_height(),
            onclose=pygame_menu.events.DISABLE_CLOSE,
            theme=play_theme,
            title="Load game",
            width=self.surface.get_width(),
        )

        for i in listdir(path.join(path.dirname(__file__), "save")):
            play_menu.add_button(i, self.load, i)

        return play_menu

    def set_selec_save(self):

        self.selected_save

    def load(self, i):
        print("Le i c'est le S sort le Rs", i)
        with open(self.path_ + i, "rb") as file:
            loaded = pickle.load(file)
        tmp = loaded["path"][0]
        tmp = tmp.split("\\")
        self.name = tmp[len(tmp) - 1]
        tmp2 = i.split(".")
        self.save_name = tmp2[0]

        print("name is : ", self.name)
        pygame.mixer.music.unload()
        self.isload = True
        print(self.isload)
