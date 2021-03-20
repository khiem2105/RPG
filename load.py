"""temporary module to load game"""
from os import path, listdir
import pickle
import pygame as pg
import settings
import map_editor_settings
from box import Button, Input
from tiledmap import Map


class Load:
    """temporary class to load game"""

    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
        settings.WIDTH = self.screen.get_width()
        settings.HEIGHT = self.screen.get_height()
        pg.display.set_caption(settings.TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.game_folder = path.dirname(__file__)
        self.map_folder = path.join(self.game_folder, "map")
        self.save_folder = path.join(self.game_folder, "save")
        self.my_maps = listdir(self.map_folder)
        self.my_saves = listdir(self.save_folder)
        self.my_buttons = dict()
        self.my_input = None
        self.state = None
        self.save_name = ""
        self.load = False
        self.name = None
        self.path_ = None
        self.map = None
        self.load_button()
        self.scroll_nbr = 0

    def load_button(self):
        """load new and load buttons"""
        if self.state == "New Game":
            for cpt, i in enumerate(self.my_maps):

                self.my_buttons[cpt] = Button(
                    settings.WIDTH // 2 - map_editor_settings.BOX_SIZE[0] // 2,
                    (
                        map_editor_settings.LOAD_POS
                        + 200
                        + map_editor_settings.BOX_SIZE[1] * (cpt + 1)
                    ),
                    map_editor_settings.BOX_SIZE,
                    name=i,
                )
            self.scroll = pg.Rect(
                settings.WIDTH // 2 - map_editor_settings.BOX_SIZE[0] // 2,
                map_editor_settings.LOAD_POS + 200 + map_editor_settings.BOX_SIZE[1],
                map_editor_settings.BOX_SIZE[0],
                map_editor_settings.BOX_SIZE[1] * 5,
            )
            self.my_input = Input(
                settings.WIDTH // 2 - map_editor_settings.BOX_SIZE[0] // 2,
                settings.HEIGHT // 4 - map_editor_settings.BOX_SIZE[1],
                map_editor_settings.BOX_SIZE,
                "Save name :",
            )
        elif self.state == "Load":
            for cpt, i in enumerate(self.my_saves):

                self.my_buttons[cpt] = Button(
                    settings.WIDTH // 2 - map_editor_settings.BOX_SIZE[0] // 2,
                    (
                        map_editor_settings.LOAD_POS
                        + 200
                        + map_editor_settings.BOX_SIZE[1] * (cpt + 1)
                    ),
                    map_editor_settings.BOX_SIZE,
                    name=i,
                )
            self.scroll = pg.Rect(
                settings.WIDTH // 2 - map_editor_settings.BOX_SIZE[0] // 2,
                map_editor_settings.LOAD_POS + 200 + map_editor_settings.BOX_SIZE[1],
                map_editor_settings.BOX_SIZE[0],
                map_editor_settings.BOX_SIZE[1] * 5,
            )

        else:
            self.my_buttons["New Game"] = Button(
                settings.WIDTH // 3 - map_editor_settings.BOX_SIZE[0] // 2,
                settings.HEIGHT // 2 - map_editor_settings.BOX_SIZE[1],
                map_editor_settings.BOX_SIZE,
                name="New Game",
            )
            self.my_buttons["Load"] = Button(
                2 * settings.WIDTH // 3 - map_editor_settings.BOX_SIZE[0] // 2,
                settings.HEIGHT // 2 - map_editor_settings.BOX_SIZE[1],
                map_editor_settings.BOX_SIZE,
                name="Load",
            )

    def events(self):
        """manage events"""
        for event in pg.event.get():
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.my_buttons.clear()
                self.my_input = None
                self.state = None
                self.load_button()
            if self.state == "New Game" or self.state == "Load":
                if self.state == "New Game":
                    self.my_input.event(event)
                buf = 5
                if len(self.my_buttons) < 5:
                    buf = len(self.my_buttons)
                for key in range(self.scroll_nbr, self.scroll_nbr + buf):
                    if self.state == "New Game":
                        if (
                            event.type == pg.MOUSEBUTTONDOWN
                            and event.button == 1
                            and self.my_buttons[key].is_cliked(event)
                        ):
                            self.path_ = path.join(
                                self.map_folder, self.my_buttons[key].text
                            )
                            self.map = Map(self.path_)
                            if self.valid_map() and len(self.my_input.text) > 0:
                                self.name = self.my_buttons[key].text
                                self.save_name = self.my_input.text
                    elif self.state == "Load":
                        if (
                            event.type == pg.MOUSEBUTTONDOWN
                            and event.button == 1
                            and self.my_buttons[key].is_cliked(event)
                        ):
                            tmp = self.my_buttons[key].text.split(".")
                            self.save_name = tmp[0]
                            self.load = True
                            path_ = path.dirname(__file__) + "/save"
                            path_ = path_ + "/" + self.save_name + ".pickle"
                            with open(path_, "rb") as file:
                                loaded = pickle.load(file)
                            tmp = loaded["path"][0]
                            tmp = tmp.split("\\")
                            self.name = tmp[len(tmp) - 1]
                if (
                    event.type == pg.MOUSEBUTTONDOWN
                    and event.button == 5
                    and self.scroll.collidepoint(event.pos)
                    and self.scroll_nbr
                    < len(self.my_buttons) - map_editor_settings.MAPNUMBER
                ):
                    self.scroll_nbr += 1
                    for key in self.my_buttons:
                        self.my_buttons[key].rect.y -= map_editor_settings.BOX_SIZE[1]
                if (
                    event.type == pg.MOUSEBUTTONDOWN
                    and event.button == 4
                    and self.scroll.collidepoint(event.pos)
                    and self.scroll_nbr > 0
                ):
                    self.scroll_nbr -= 1
                    for key in self.my_buttons:
                        self.my_buttons[key].rect.y += map_editor_settings.BOX_SIZE[1]
            else:
                if (
                    event.type == pg.MOUSEBUTTONDOWN
                    and event.button == 1
                    and self.my_buttons["New Game"].is_cliked(event)
                ):
                    self.state = "New Game"
                    self.my_buttons.clear()
                    self.load_button()
                elif (
                    event.type == pg.MOUSEBUTTONDOWN
                    and event.button == 1
                    and self.my_buttons["Load"].is_cliked(event)
                ):
                    self.state = "Load"
                    self.my_buttons.clear()
                    self.load_button()
            if event.type == pg.QUIT:
                pg.quit()

    def get_map(self, string):
        """get map name"""
        self.name = string

    def draw(self):
        """draw menu"""
        self.screen.fill((100, 100, 100))
        if self.state == "New Game" or self.state == "Load":
            buf = 5
            if len(self.my_buttons) < 5:
                buf = len(self.my_buttons)
            for i in range(self.scroll_nbr, self.scroll_nbr + buf):
                self.screen.blit(
                    self.my_buttons[i].name_surface,
                    (self.my_buttons[i].rect.x + 5, self.my_buttons[i].rect.y),
                )
            if self.state == "New Game":
                self.my_input.draw(self.screen)
        else:
            for key in self.my_buttons:
                self.screen.blit(
                    self.my_buttons[key].name_surface,
                    (self.my_buttons[key].rect.x + 5, self.my_buttons[key].rect.y),
                )
        pg.display.flip()

    def valid_map(self):
        """check if map is valid"""
        with open(self.path_) as map_file:
            map_file.seek(self.map.offset, 0)
            tmp = map_file.read()
            tmp = tmp.split(" ")
            try:
                if tmp[1] != "valid":
                    return False
            except IndexError:
                return False
            else:
                return True
