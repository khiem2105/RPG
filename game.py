"""main file"""
from os import path
import sys
import pygame as pg
import settings
from combat_log import Log
from tiledmap import Map, Camera
from draw import draw, draw_reachable
from quest import Quest
from event import events, new
from item import Itemlist

vec = pg.math.Vector2


class Game:
    """Main class that contains everything"""

    def __init__(self, save_name, editor=False, name="", chara_dic=None):
        """initialize all variable that the class Game contains"""
        pg.init()
        if not editor:
            self.screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
            settings.WIDTH = self.screen.get_width()
            settings.HEIGHT = self.screen.get_height()
        self.background = pg.Surface((100 * settings.TILESIZE, 100 * settings.TILESIZE))
        self.f_background = pg.Surface(
            (100 * settings.TILESIZE, 100 * settings.TILESIZE), pg.SRCALPHA, 32
        )
        pg.display.set_caption(settings.TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.playing = False
        self.all_item = Itemlist().item_list
        self.save_name = save_name
        self.chara_dic = chara_dic
        self.first = True
        self.pause = False
        self.is_console_opened = False
        self.shortcut = False
        self.bind = {
            "spell 1": pg.K_a,
            "spell 2": pg.K_z,
            "spell 3": pg.K_e,
            "map": pg.K_SEMICOLON,
            "turn": pg.K_p,
            "player 1": pg.K_F1,
            "player 2": pg.K_F2,
            "player 3": pg.K_F3,
            "inventory": pg.K_i,
            "player sheet": pg.K_SPACE,
        }
        self.buttons = {}
        self.inputs = {}
        self.game_folder = ""
        self.map_folder = ""
        self.img_folder = ""
        self.path_ = {}
        self.name = name
        self.map = None
        self.img = {}
        self.m_img = {}
        self.img_path = {
            "Pa": settings.PATH_IMG,
            "V": settings.VOID_IMG,
            "P": settings.PLAYER_IMG,
            "Wiz": settings.WIZARD_IMG,
            "Bar": settings.BARBARIAN_IMG,
            "Rog": settings.ROGUE_IMG,
            "W": settings.WALL_IMG,
            "G": settings.GROUND_IMG,
            "R": settings.REACHABLE_IMG,
            "AOE": settings.AOE_TILE_IMG,
            "ZO": settings.ZOMBIE_IMG,
            "H": settings.HEAL_SKILL,
            "Ve": settings.VOID_EDITOR_IMG,
            "Po": settings.PORTAL_IMG,
            "BP": settings.BACK_PORTAL_IMG,
            "ZG": settings.ZOMBIE_GROUND_IMG,
            "SK": settings.SKELETON_IMG,
            "MI": settings.MINOTAUR_IMG,
            "GO": settings.GOBLIN_IMG,
            "WO": settings.WOLF_IMG,
            "J": settings.PNJ_IMG,
            "M": settings.MERCHANT_IMG,
            "C": settings.CONTAINER_IMG,
        }
        self.current_level = 0
        self.load_data()
        if not editor:
            self.valid_map()
        self.sprites = {}
        self.mmap_group = {}
        self.mmap = False
        self.players = {"Barbarian": None, "Wizard": None, "Rogue": None}
        self.player = None
        self.focus = None
        self.camera = Camera(self.map.width, self.map.height)
        self.quest = Quest()
        self.m_current_level = 0
        self.camera_pos = (0, 0)
        self.enemy = {}
        self.attributed_to_enemy = []
        self.portal_pos = {}
        self.prow = {}
        self.pcol = {}
        self.grid = {}
        self.tick = 0
        self.click = ""
        self.g_score = {}
        self.f_score = {}
        self.editor = editor
        if not editor:
            self.log = {}
            self.log["log"] = Log(
                300, 200, (settings.WIDTH - 300, 10), settings.BLACK, 26, self
            )
            self.log["log"].add_log("Combat Log")
            self.log["log"].print_log(self.screen)
            self.log["quest"] = Log(
                300,
                200,
                (settings.WIDTH - 300, self.log["log"].height + 10),
                settings.WHITE,
                26,
                self,
                False,
            )
            self.log["quest"].print_log(self.screen)

    def valid_map(self):
        """
        check if the map is valid before load it.
        It avoids the user to load a corrupted map that makes the game crash.
        """
        with open(self.path_[self.current_level]) as map_file:
            map_file.seek(self.map.offset, 0)
            tmp = map_file.read()
            tmp = tmp.split(" ")
            try:
                if tmp[1] != "valid":
                    self.quit()
            except IndexError:
                self.quit()

    def load_data(self):
        """load data from folder img and map"""
        self.game_folder = path.dirname(__file__)
        self.map_folder = path.join(self.game_folder, "map")
        self.img_folder = path.join(self.game_folder, "img")
        if self.name:
            self.path_[self.current_level] = path.join(self.map_folder, self.name)
        else:
            self.path_[self.current_level] = path.join(self.map_folder, "map1.txt")
        self.map = Map(self.path_[self.current_level])
        for key in self.img_path:
            if any(
                self.img_path[key] == self.img_path[i]
                for i in ["P", "Wiz", "Bar", "Rog"]
            ):
                self.img[key] = pg.image.load(
                    path.join(self.img_folder, self.img_path[key])
                ).convert_alpha()
            elif (
                self.img_path[key] == self.img_path["J"]
                or self.img_path[key] == self.img_path["M"]
            ):
                continue
            else:
                self.img[key] = pg.image.load(
                    path.join(self.img_folder, self.img_path[key])
                ).convert_alpha()
                self.m_img[key] = pg.image.load(
                    path.join(self.img_folder, self.img_path[key])
                ).convert_alpha()
            if any(
                self.img_path[key] == self.img_path[i]
                for i in ["P", "Wiz", "Bar", "Rog"]
            ) or any(
                self.img_path[key] == self.img_path[i]
                for i in ["ZO", "SK", "MI", "GO", "WO"]
            ):
                self.img[key] = pg.transform.scale(
                    self.img[key],
                    (int(0.9 * settings.TILESIZE), int(0.9 * settings.TILESIZE)),
                )
            else:
                self.img[key] = pg.transform.scale(
                    self.img[key], (settings.TILESIZE, settings.TILESIZE)
                )
                self.m_img[key] = pg.transform.scale(self.img[key], (10, 10))

    def change_map(self):
        """
        Method that allow the user to change map.
        It checks if the map has already been load or not.
        """
        self.current_level += 1
        self.m_current_level = self.current_level
        self.map = Map(path.join(self.map_folder, self.path_[self.current_level]))
        self.camera = Camera(self.map.width, self.map.height)
        self.background.fill(settings.BLACK)
        if len(self.path_) == self.current_level + 1:
            self.attributed_to_enemy = []
            new(self)
            draw_reachable(self)
        else:
            self.player.pos = vec(
                (self.pcol[self.current_level] + 0.5) * settings.TILESIZE,
                (self.prow[self.current_level] + 0.5) * settings.TILESIZE,
            )

            self.map = Map(path.join(self.map_folder, self.path_[self.current_level]))
            self.camera = Camera(self.map.width, self.map.height)
            self.first = True
            self.camera.update(self.focus)
            self.update()

    def run(self):
        """game loop - set self.playing = False to end the game"""
        self.playing = True
        while self.playing:
            self.tick = self.clock.tick(settings.FPS) / 1000
            if self.tick > 0.02:
                self.tick = 0.017
            events(self)

            if not self.mmap and not self.pause:
                self.update()

            draw(self)

    @staticmethod  # function does not need an instance of game
    def quit():
        """end the program"""
        pg.quit()
        sys.exit()

    def update(self):
        """update the player and the camera (positions), update portion of the game loop"""
        if self.first:
            self.sprites[self.current_level]["A"].update()
        self.camera.update(self.focus)
        self.sprites[self.current_level]["A"].update()

    def show_start_screen(self):
        """need to be define"""

    def show_go_screen(self):
        """need to be define"""
