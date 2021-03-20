""""Map editor module that allows to create new map"""
import sys
import shutil
import os
from os import path, stat, listdir
import pygame
from event import new as enew
from pnj import Pnj
from settings import TILESIZE
from player import Player
from enemy import Enemy
from game import Game
from box import Button, Input
import map_editor_settings
import sprites
import settings
from tiledmap import Map, Camera

pygame.mouse.set_visible = True


class MapEditor:
    """Map editor class"""

    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        settings.WIDTH = self.window.get_width()
        settings.HEIGHT = self.window.get_height()
        pygame.display.set_caption("Map editor")
        self.window = pygame.display.get_surface()
        self.screen = pygame.display.get_surface()
        self.game_folder = path.dirname(__file__)
        self.map_folder = path.join(self.game_folder, "map")
        self.img_folder = path.join(self.game_folder, "img")
        self.name = "mapdefault.txt"
        self.path = path.join(self.map_folder, "mapdefault.txt")
        self.path_ = {}

        # self.new_name = path.join(self.map_folder, self.get_name())
        self.map_write = open(path.join(self.map_folder, "mapdefault.txt"), "a")
        self.map_write.seek(0)
        self.map = None
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
            "M": settings.PNJ_IMG,
            "C": settings.CONTAINER_IMG,
        }
        self.img = {}
        self.sprites = {0: {"A": pygame.sprite.Group()}}
        self.mmap_group = {0: pygame.sprite.Group()}
        self.current_level = 0
        self.camera = Camera(settings.WIDTH, settings.HEIGHT)
        self.camera_pos = (0, 0)
        self.player = None
        self.m_current_level = 0
        self.player_pos = None
        self.portal = None
        self.editor = True
        self.portal_pos = None
        self.valid = True
        self.mouse_editor = False
        self.mouse_tile = False
        self.tile_width = TILESIZE
        self.tile_height = TILESIZE
        self.left = 0
        self.top = 0
        self.mybool = False
        self.my_maps = listdir(self.map_folder)
        self.my_tiles = listdir(self.img_folder)
        self.test = dict(self.load_tiles())
        self.my_butons = dict()
        self.tile_id = 0
        self.scroll = None
        self.scroll_nbr = 0
        self.is_resized = False
        self.display_setup()
        self.tilecpt = 0
        self.name_path = ""

    # FONCTION POUR GERER LES DIFFERENTS DISPLAY (entre le tile set et l'endroit de la peinture)
    # ça setup le début hihi

    def load_data(self):
        """load data from path image"""
        if stat(self.path).st_size == 0:
            self.new()
        self.map = Map(self.path)
        Game.load_data(self)

    def load_map(self):
        """load data from map if it exist"""
        if stat(self.path).st_size == 0 or self.name == "mapdefault.txt":
            self.new()
        self.map = Map(self.path)
        self.map_name_text.text = self.name
        for key in self.sprites[0]:
            self.sprites[0][key].empty()
        if self.portal:
            self.portal = None
            self.portal_pos = None
        for row, tiles in enumerate(self.map.edata):
            for col, tile in enumerate(tiles):
                if tile == "0":
                    sprites.Void_editor(self, col, row)
                if tile == "1":
                    sprites.Wall(self, col, row)
                if tile == ".":
                    sprites.Ground(self, col, row)
                if tile == "M":
                    Pnj(self, col, row, True)
                if tile == "J":
                    Pnj(self, col, row, False)
                if tile == "P":
                    self.player = sprites.Path(self, col, row)
                    self.player_pos = (col, row)
                if tile == "X":
                    file = open(self.path, "r")
                    tmp_map = Map(self.path)
                    file.seek(tmp_map.offset, 0)
                    line_map = file.read()
                    new_line = line_map.split(" ")
                    self.portal_name_text.text = new_line[0]
                    self.portal = sprites.Portal(self, col, row, "")
                    self.portal_pos = (col, row)

        try:
            default = path.join(self.map_folder, "mapdefault.txt")
            shutil.copyfile(self.path, default)
            self.map = Map(default)
        except shutil.SameFileError:
            pass

    def display_setup(self):
        """[Setup the display in 3 part tileset,paint,parameters]

        A CHANGER LES 768 EN WINDOWS[1] une fois qu'on aura import les settings
        """

        self.tileset_window = pygame.Surface((4 * TILESIZE, self.window.get_height()))
        self.tileset_window.fill((200, 200, 200))
        self.tile_gride = self.draw_tile_gride(self.tileset_window)

        # A réléchir si on augmente le spacing d'une tiles ou plus !
        self.first_spacing = self.tileset_window.get_width() - 2 * TILESIZE

        self.center_distance_width = self.tileset_window.get_width() + (
            self.tile_width * 2
        )
        self.map_paint_width = self.window.get_width() - (
            self.tileset_window.get_width() + self.first_spacing * 5 + TILESIZE
        )

        self.map_paint_window = pygame.Surface(
            ((self.map_paint_width + 2 * TILESIZE), self.window.get_height())
        )
        self.map_paint_window.fill((200, 200, 200))
        self.map_paint_gride = self.draw_tile_gride(self.map_paint_window)

        self.second_spacing = (
            self.tileset_window.get_width()
            + self.map_paint_window.get_width()
            - 2 * TILESIZE
        )
        self.param_window_width = (
            self.map_paint_window.get_width()
            + self.tileset_window.get_width()
            + self.first_spacing * 2
        )

        self.param_window = pygame.Surface(
            ((self.param_window_width), self.window.get_height())
        )
        self.param_window.fill((200, 200, 200))
        self.param_window_gride = self.draw_tile_gride(self.param_window)

        self.map_name_text = Input(
            self.param_window_width + 10,
            map_editor_settings.MAP_NAME_IMPUT,
            map_editor_settings.BOX_SIZE,
            name="Map name :",
            text="",
        )

        self.portal_name_text = Input(
            self.param_window_width + 10,
            map_editor_settings.PORTAL_NAME_IMPUT,
            map_editor_settings.BOX_SIZE,
            name="Portal name :",
            text="",
        )

        self.load_button = Button(
            self.param_window_width + 10,
            map_editor_settings.LOAD_POS,
            map_editor_settings.BOX_SIZE,
            name="Load Map",
        )
        self.load_button2()

        self.validation_button = Button(
            self.param_window_width + 10,
            map_editor_settings.VALID_MAP_POS,
            map_editor_settings.BOX_SIZE,
            name="Validation",
        )
        self.validation_button.color = pygame.Color(128, 0, 0)
        self.validation_button.name_surface = pygame.font.SysFont(
            "Cascadia code", 32
        ).render(self.validation_button.text, True, self.validation_button.color)

        self.screen.fill((10, 10, 10))
        self.map_paint_window.fill((255, 255, 255))
        self.tileset_window.fill((255, 255, 255))
        self.param_window.fill((200, 200, 200))
        self.screen.blit(self.tile_gride, (0, 0))
        self.tileset_window.blit(self.tile_gride, (0, 0))

    def get_name(self):
        """getter of the text of the butto,

        Returns:
            string: name of the map
        """
        return self.map_name_text.text

    def get_button_name(self, cpt):
        """get button name"""
        text = self.my_butons[cpt - 1].name
        return text

    def draw_tile_gride(self, window):
        """Draw a gride on the window passed in parameters

        Args:
            window (Surface): Surface where we need to draw the gride

        Returns:
            surface: a surface with the gride
        """
        my_display = window.copy()
        my_display.set_colorkey((255, 255, 255))
        left = 0
        top = 0
        x_pos = self.tile_width
        y_pos = self.tile_height
        while top < my_display.get_height():
            while left < my_display.get_width():
                pygame.draw.rect(
                    my_display, (140, 140, 140), pygame.Rect(left, top, x_pos, y_pos), 1
                )
                left = left + x_pos
            left = 0
            top = top + y_pos

        return my_display

    def draw(self):
        """[draw new sprites]
        Will be deleted soon
        """
        self.camera.camera = pygame.Rect(
            self.camera.x, self.camera.y, settings.WIDTH, settings.HEIGHT
        )
        self.sprites["A"].update()
        for sprite in self.sprites["A"]:
            self.window.blit(sprite.image, self.camera.apply(sprite))

    def drawbis(self):
        """Draw all our surfaces and the gride if needed,
        also draw and update sprites et camera check"""

        self.display_tile(self.tileset_window)

        self.camera.camera = pygame.Rect(
            self.camera.x, self.camera.y, settings.WIDTH, settings.HEIGHT
        )
        for sprite in self.sprites[0]["A"]:
            if (
                -self.camera.x - settings.WIDTH * 0.4
                <= sprite.rect.x
                <= -self.camera.x + settings.WIDTH * 1.4
                and -self.camera.y - settings.HEIGHT * 0.4
                <= sprite.rect.y
                <= -self.camera.y + settings.HEIGHT * 1.4
            ):
                sprite.update()
                self.map_paint_window.blit(sprite.image, self.camera.apply(sprite))

        self.screen.blit(self.tileset_window, (0, 0))
        self.screen.blit(
            self.param_window, ((self.center_distance_width + self.second_spacing), 0)
        )
        self.screen.blit(self.map_paint_window, (self.center_distance_width, 0))

        self.map_name_text.draw(self.screen)
        if self.portal:
            self.portal_name_text.draw(self.screen)
        else:
            self.portal_name_text.text = ""

        self.screen.blit(
            self.load_button.name_surface,
            (self.load_button.rect.x + 5, self.load_button.rect.y),
        )

        if self.mybool:
            for i in range(self.scroll_nbr, self.scroll_nbr + 5):
                self.screen.blit(
                    self.my_butons[i].name_surface,
                    (self.my_butons[i].rect.x + 5, self.my_butons[i].rect.y),
                )
        self.validation_button.name_surface = pygame.font.SysFont(
            "Cascadia code", 32
        ).render(self.validation_button.text, True, self.validation_button.color)
        self.screen.blit(
            self.validation_button.name_surface,
            (self.validation_button.rect.x + 5, self.validation_button.rect.y),
        )

        pygame.display.flip()

    def load_tiles(self):
        """load all tiles with a index in a dictionary

        Yields:
            [type]: [description]
        """
        for cpt, i in enumerate(listdir(path.join(self.img_folder, "tiles"))):
            yield (
                cpt + 1,
                pygame.image.load(path.join(path.join(self.img_folder, "tiles"), i)),
            )

    def display_tile(self, surface):
        """Display all the tiles in the dictionary of tiles in the tileset windows

        Args:
            surface (surface): surface where we are going to blit all the tiles
        """

        self.tilecpt = 0
        for cpt in range(len(listdir(self.img_folder))):
            for j in range(surface.get_width() // TILESIZE):
                self.tilecpt += 1
                if self.tilecpt <= len(listdir(path.join(self.img_folder, "tiles"))):
                    surface.blit(
                        pygame.transform.scale(self.test[self.tilecpt], (36, 36)),
                        (self.tile_width * j, self.tile_height * cpt),
                    )

    def get_id_tiles(self):
        """Return id of the tile in the tile set located a the positon of the mouse

        Returns:
            int : number of the tile (if it's return 43, it's the 43 tiles in our repository)
        """
        xpos, ypos = self.mouse_pos_tile()
        if ypos * 4 + xpos < len(listdir(path.join(self.img_folder, "tiles"))):
            return listdir(path.join(self.img_folder, "tiles"))[ypos * 4 + xpos]
        else:
            return 0

    def save_map(self):
        """save the map with the name if you press p !"""
        _ = self.map_name_text.text.split(".")
        try:
            if _[1] != "txt":
                self.map_name_text.text = _[0] + ".txt"
        except IndexError:
            self.map_name_text.text += ".txt"
        self.path = path.join(self.map_folder, self.map_name_text.text)
        self.name_path = path.join(self.map_folder, "mapdefault" + ".txt")
        if self.map_name_text.text:
            file = open(self.name_path, "a+")
            _ = open(self.path, "a+")
            tmp_map = Map(self.name_path)
            self.test_map()
            if self.portal:
                file.seek(tmp_map.offset, 0)
                file.truncate()
                file.write(self.portal_name_text.text)
            else:
                file.seek(tmp_map.offset, 0)
                file.truncate()
                file.write("m")
            if self.valid:
                file.write(" valid")

            file.close()
            try:
                shutil.copyfile(self.name_path, self.path)
            except shutil.SameFileError:
                pass
        else:
            self.valid = False

    def load(self, button=None):
        """load method"""
        if button is None:
            self.path = path.join(self.map_folder, self.get_name() + ".txt")
            self.name = self.get_name() + ".txt"
        else:
            self.path = path.join(self.map_folder, button.text)
            self.name = button.text
        self.camera.y = 0
        self.camera.x = 0
        self.load_map()

    def load_button2(self):
        """generate all the load button parameters (the list of maps)"""
        for cpt, i in enumerate(self.my_maps):

            self.my_butons[cpt] = Button(
                self.param_window_width + 10,
                (
                    map_editor_settings.LOAD_POS
                    + map_editor_settings.BOX_SIZE[1] * (cpt + 1)
                ),
                map_editor_settings.BOX_SIZE,
                name=i,
            )
        self.scroll = pygame.Rect(
            self.param_window_width,
            map_editor_settings.LOAD_POS + map_editor_settings.BOX_SIZE[1],
            map_editor_settings.BOX_SIZE[0],
            map_editor_settings.BOX_SIZE[1] * 5,
        )

    def slide_up(self):
        """slide up the map editor if we're not at the top of the map"""
        if -self.camera.y > 0:
            self.camera.y += self.tile_height

    # même chose si on va en bas

    def slide_down(self):
        """slide down the map editor"""
        self.camera.y -= self.tile_height

    def slide_right(self):
        """slide right the map editor"""
        self.camera.x -= self.tile_width

    def slide_left(self):
        """slide left the map editor if we're not at the edge of the map"""
        if -self.camera.x > 0:
            self.camera.x += self.tile_height

    def reset_default_map(self):
        """Reset default map,after saving (doesn't work well yet)"""
        for _ in range(100):
            for _ in range(100):
                file = open(self.path, "w")
                file.write("0")

    def new(self):
        """generate a new map with only void"""
        file = open(self.path, "r+")
        file.truncate(0)
        for _ in range(100):
            for _ in range(100):
                file.write("0")
            file.write("\n")

    def fwrite(self, string):
        """Write in a txt in order to save our map

        Args:
            string (string): tiles names in order to know what char to write in the txt
        """
        xpos, ypos = self.mouse_pos_tile()
        if xpos < 100 and ypos < 100:
            off = 0
            self.map_write = open(path.join(self.map_folder, "mapdefault.txt"), "r+")
            for i in range(ypos):
                off += self.map.line_length[i]

            self.map_write.seek((xpos + off), 0)
            if self.map_write.read(1) == "X":
                self.sprites[0]["A"].remove(self.portal)
                self.portal = None
                self.portal_pos = None
                sprites.Void_editor(self, xpos, ypos)
            self.map_write.seek(self.map_write.tell() - 1, os.SEEK_SET)

            if string == "Wall":
                self.map_write.write("1")
                self.map_write.close()
                sprites.Wall(self, xpos, ypos)
            elif string == "Ground":
                self.map_write.write(".")
                self.map_write.close()
                sprites.Ground(self, xpos, ypos)
            elif string == "Player":
                if self.player:
                    self.sprites[0]["A"].remove(self.player)
                    sprites.Void_editor(self, self.player_pos[0], self.player_pos[1])
                    _off = 0
                    for i in range(self.player_pos[1]):
                        _off += self.map.line_length[i]
                    self.map_write.seek(self.player_pos[0] + _off, 0)
                    self.map_write.write("0")
                self.map_write.seek((xpos + off), 0)
                self.map_write.write("P")
                self.player = Player(self, xpos, ypos)
                self.player_pos = (xpos, ypos)
                self.map_write.close()
            elif string == "Portal":
                if self.portal:
                    self.sprites[0]["A"].remove(self.portal)
                    sprites.Void_editor(self, self.portal_pos[0], self.portal_pos[1])
                    _off = 0
                    for i in range(self.portal_pos[1]):
                        _off += self.map.line_length[i]
                    self.map_write.seek(self.portal_pos[0] + _off, 0)
                    self.map_write.write("0")
                self.map_write.seek((xpos + off), 0)
                self.map_write.write("X")
                self.portal = sprites.Portal(self, xpos, ypos, "test")
                self.portal_pos = (xpos, ypos)
                self.map_write.close()
            elif string == "Void":
                self.map_write.write("0")
                self.map_write.close()
                sprites.Void_editor(self, xpos, ypos)
            elif string == "Merchant":
                self.map_write.write("M")
                self.map_write.close()
                Pnj(self, xpos, ypos, True)
            elif string == "Pnj":
                self.map_write.write("J")
                self.map_write.close()
                Pnj(self, xpos, ypos, False)
            elif string == "Boss":
                self.map_write.write("B")
                self.map_write.close()
                Enemy(self, xpos, ypos, 10)

    def mouse_position(self):
        """Absolute positon of the mouse in pxm

        Returns:
            [tuples of int]
        """
        mousex, mousey = pygame.mouse.get_pos(self)
        return mousex, mousey

    def mouse_pos_tile(self):
        """Returns the mouse pos in tiles (usefull for drawing)

        Returns:
            [tuples of int]:
        """
        mousex, mousey = self.mouse_position()
        if (
            (self.center_distance_width)
            <= mousex
            <= (self.center_distance_width + self.second_spacing)
        ):
            if not self.mouse_editor:
                self.mouse_editor = True
                self.mouse_tile = False
            return (
                (
                    (
                        mousex
                        - self.camera.x
                        - self.tileset_window.get_width()
                        - self.first_spacing
                    )
                    // self.tile_width
                )
            ), (((mousey - self.camera.y) // self.tile_height))
        elif 0 <= mousex <= self.tileset_window.get_width():
            if not self.mouse_tile:
                self.mouse_tile = True
                self.mouse_editor = False
            return ((mousex // self.tile_width), (mousey // self.tile_height))

        else:
            if self.mouse_editor:
                self.mouse_editor = False
            if self.mouse_tile:
                self.mouse_tile = False
            return (0, 0)

    def input(self):
        """
        event management function
        """

        keys = pygame.key.get_pressed()
        if not self.map_name_text.istyping and not self.portal_name_text.istyping:
            if keys[pygame.K_DOWN]:
                self.slide_down()
            if keys[pygame.K_UP]:
                self.slide_up()
            if keys[pygame.K_RIGHT]:
                self.slide_right()
            if keys[pygame.K_LEFT]:
                self.slide_left()
        mouse = pygame.mouse.get_pressed()
        tile = map_ed.tile_id
        if self.mouse_editor:
            if mouse[0]:
                if tile == "ground.png":
                    self.fwrite("Ground")
                    self.valid = False
                    self.validation_button.color = settings.RED
                if tile == "tile.png":
                    self.fwrite("Wall")
                    self.valid = False
                    self.validation_button.color = settings.RED
                if tile == "player.png":
                    self.fwrite("Player")
                    self.valid = False
                    self.validation_button.color = settings.RED
                if tile == "portal.png":
                    self.fwrite("Portal")
                    self.valid = False
                    self.validation_button.color = settings.RED
                if tile == "void_editor.png":
                    self.fwrite("Void")
                    self.valid = False
                    self.validation_button.color = settings.RED
                if tile == "merchant.png":
                    self.fwrite("Merchant")
                    self.valid = False
                    self.validation_button.color = settings.RED
                if tile == "pnj.png":
                    self.fwrite("Pnj")
                    self.valid = False
                    self.validation_button.color = settings.RED
                if tile == "Minotaur.png":
                    self.fwrite("Boss")
                    self.valid = False
                    self.validation_button.color = settings.RED
        for event in pygame.event.get():
            if self.valid and event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                self.map_write.close()
                pygame.quit()
                sys.exit()
            if event.type == pygame.VIDEORESIZE:
                self.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                self.display_setup()
            self.map_name_text.event(event)
            self.portal_name_text.event(event)
            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and self.load_button.is_cliked(event)
            ):
                self.mybool = not self.mybool
            if self.mybool:
                for key in range(self.scroll_nbr, self.scroll_nbr + 5):
                    if (
                        event.type == pygame.MOUSEBUTTONDOWN
                        and event.button == 1
                        and self.my_butons[key].is_cliked(event)
                    ):
                        self.load(self.my_butons[key])
                if (
                    event.type == pygame.MOUSEBUTTONDOWN
                    and event.button == 4
                    and self.scroll.collidepoint(event.pos)
                    and self.scroll_nbr > 0
                ):
                    self.scroll_nbr -= 1
                    for key in self.my_butons:
                        self.my_butons[key].rect.y += map_editor_settings.BOX_SIZE[1]
                if (
                    event.type == pygame.MOUSEBUTTONDOWN
                    and event.button == 5
                    and self.scroll.collidepoint(event.pos)
                    and self.scroll_nbr
                    < len(self.my_butons) - map_editor_settings.MAPNUMBER
                ):
                    self.scroll_nbr += 1
                    for key in self.my_butons:
                        self.my_butons[key].rect.y -= map_editor_settings.BOX_SIZE[1]
            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and self.validation_button.is_cliked(event)
            ):
                self.save_map()
                if self.valid:
                    self.validation_button.color = settings.GREEN
                else:
                    self.validation_button.color = settings.RED
            if event.type == pygame.MOUSEBUTTONDOWN and self.mouse_tile:
                self.tile_id = self.get_id_tiles()

    def test_map(self):
        """Is our mal valid"""
        try:
            self.map = Map(self.path)
            mgame = Game(True, self.name)
            enew(mgame)

        except (AttributeError, IndexError):
            self.valid = False
        else:
            if (
                self.portal
                and not os.path.exists(
                    path.join(self.map_folder, self.portal_name_text.text)
                )
            ) or len(self.map.data) == 0:
                self.valid = False
            elif self.portal:
                self.valid = True

            else:
                self.valid = True


RUNNING = True
map_ed = MapEditor()
map_ed.load_data()
map_ed.load_map()

while RUNNING:
    map_ed.mouse_pos_tile()
    map_ed.input()
    map_ed.drawbis()

    #
    pygame.display.flip()

pygame.quit()
