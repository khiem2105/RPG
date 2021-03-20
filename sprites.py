"""This file manage the sprites[game.current_level] frome the game and how they are define"""
import pygame as pg
import settings
from pathfinding import Node

vec = pg.math.Vector2


class Tile(pg.sprite.Sprite):
    """Default class : in fact never used"""

    def __init__(self, game, x, y):
        """initialise variable"""
        self.groups = game.sprites[game.current_level]["A"]
        pg.sprite.Sprite.__init__(self, self.groups)
        self.node = Node(game, y, x)
        self.game = game
        self.image = game.img["V"]
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * settings.TILESIZE
        self.rect.y = y * settings.TILESIZE

    # def update_id(self, id):
    #     self.game.sprites[self.game.current_level]["MM"].remove(self)
    #     self.image = self.game.img[id]
    #     MMap(self.game, self.x, self.y, self.image)


class MMap(pg.sprite.Sprite):
    def __init__(self, game, x, y, img):
        self.groups = game.mmap_group[game.m_current_level]
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = 10 * x
        self.rect.y = 10 * y


class Fog_of_War(Tile):
    """fog that hide the area not previously visited"""

    def __init__(self, game, x, y, tipe, alpha=255):
        super().__init__(game, x, y)
        self.image = pg.Surface((settings.TILESIZE, settings.TILESIZE))
        self.m_image = pg.Surface((10, 10))
        self.alpha = alpha
        self.image.fill(settings.BLACK)
        self.m_image.fill(settings.BLACK)
        self.image.set_alpha(alpha)
        self.m_image.set_alpha(alpha)
        self.tipe = tipe
        self.map = MMap(game, x, y, self.m_image)


class Wall(Tile):
    """Wall"""

    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.image = game.img["W"]
        self.map = MMap(game, x, y, game.m_img["W"])
        self.node.make_barrier()


class Void_editor(Tile):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.image = game.img["Ve"]
        self.map = MMap(game, x, y, game.m_img["Ve"])


class Void(Tile):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.image = game.img["Ve"]
        self.image.fill(settings.BLACK)


class Ground(Tile):
    """Ground"""

    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.image = game.img["G"]
        self.map = MMap(game, x, y, game.m_img["G"])


class Zombie_ground(Tile):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.image = game.img["ZG"]
        self.map = MMap(game, x, y, game.m_img["ZG"])


class AOE_zone(Tile):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.image = game.img["AOE"]


class Path(Tile):
    """Path that will be draw"""

    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.image = game.img["Pa"]


class Portal(Tile):
    def __init__(self, game, x, y, name):
        super().__init__(game, x, y)
        self.image = game.img["Po"]
        self.map = MMap(game, x, y, game.m_img["Po"])
        self.map_name = name


class Back_Portal(Tile):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.image = game.img["BP"]
        self.map = MMap(game, x, y, game.m_img["BP"])


class ShotSkill(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        # self._layer = EFFECTS_LAYER
        self.groups = (
            game.sprites[game.current_level]["A"],
            game.sprites[game.current_level]["S"],
        )
        pg.sprite.Sprite.__init__(self, self.groups)
        self.node = Node(game, y, x)
        self.game = game
        self.size = 40
        self.image = pg.transform.scale(game.img["H"], (self.size, self.size))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y


class HealSkill(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        # self._layer = EFFECTS_LAYER
        self.groups = (
            game.sprites[game.current_level]["A"],
            game.sprites[game.current_level]["S"],
        )
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.size = 40
        self.image = pg.transform.scale(game.img["H"], (self.size, self.size))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def update_id(self, item_id):
        self.game.sprites[self.game.current_level]["MM"].remove(self)
        self.image = self.game.img[item_id]
        MMap(self.game, self.x, self.y, self.image)


class CoolDown(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        # self._layer = EFFECTS_LAYER
        self.groups = (
            game.sprites[game.current_level]["A"],
            game.sprites[game.current_level]["S"],
        )
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.size = 40
        self.image = pg.Surface((self.size, self.size))
        fill(self.image, settings.LIGHTGREY)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y


def fill(surface, color):
    """Fill all pixels of the surface with color, preserve transparency."""
    w, h = surface.get_size()
    r, g, b = color
    for x in range(w):
        for y in range(h):
            surface.set_at((x, y), (r, g, b))


def draw_outline_rect(surf, x, y, length):
    outline_rect = pg.Rect(x, y, length, length)
    pg.draw.rect(surf, settings.WHITE, outline_rect, 2)
