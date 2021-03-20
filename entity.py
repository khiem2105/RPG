"""Module that contains Entity class : the superclass from player and entity"""
import pygame as pg
import settings

vec = pg.math.Vector2


class Entity(pg.sprite.Sprite):
    """class entity"""

    def __init__(self, game, x_pos, y_pos):
        """initialise all the variables that the entity will need"""
        self.game = game
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.image = game.img["P"]  # default value
        self.image.set_colorkey(settings.BLACK)
        self.rect = self.image.get_rect()
        self.vel = vec(0, 0)
        self.pos = vec(x_pos + 0.5, y_pos + 0.5) * settings.TILESIZE
        self.rot = 0
        self.target = vec(0, 0)
        self.inmovement = False
        self.path = []
        self.mask = pg.mask.from_surface(self.image)
        self.current_node_pos = None
        self.current_node = None
        self.bmove = False
        self.asmove = False
        self.level = 1
        self.reach_draw = False
        self.health = settings.PLAYER_HEALTH
        self.mana = settings.PLAYER_MANA
        self.turn = 0
        self.groups = game.sprites[game.current_level]["A"]
        pg.sprite.Sprite.__init__(self, self.groups)

    def get_current_position(self, lvl):
        """return the node where the player is currently at"""
        return self.game.grid[lvl][int(self.pos.y / settings.TILESIZE)][
            int(self.pos.x / settings.TILESIZE)
        ]

    def reset(self):
        """reset entity variable"""
        self.vel = vec(0, 0)
        self.rot = 0
        self.target = vec(0, 0)
        self.inmovement = False
        self.path = []

    def move(self):
        """describe how the player will follow the path"""
        if not self.inmovement and self.path and self.bmove:
            self.bmove = False
            self.inmovement = True
            self.current_node = self.path.pop(0)
            self.current_node_pos = self.current_node.get_pos()
            self.target = vec(self.current_node_pos)
            self.rot = (self.target - self.pos).angle_to(vec(1, 0))
            self.vel = vec(settings.PLAYER_SPEED, 0).rotate(-self.rot)
        elif (
            self.inmovement
            and (
                (
                    abs(self.target.x - self.pos.x) <= settings.DELTA
                    and abs(self.target.y - self.pos.y) <= settings.DELTA
                )
            )
            and self.path
        ):
            # if delta max is equal to 1, glitch can append.
            # if delta max is superior to 5 collision with wall occure

            self.asmove = True
            self.current_node = self.path.pop(0)
            self.current_node_pos = self.current_node.get_pos()
            self.target = vec(self.current_node_pos)
            self.rot = (self.target - self.pos).angle_to(vec(1, 0))
            self.vel = vec(settings.PLAYER_SPEED, 0).rotate(-self.rot)
        elif (
            self.inmovement
            and (
                (
                    abs(self.target.x - self.pos.x) <= settings.DELTA
                    and abs(self.target.y - self.pos.y) <= settings.DELTA
                )
            )
            and not self.path
        ):
            self.asmove = True
            self.vel = vec(0, 0)
            self.inmovement = False
            self.reach_draw = True
        elif (self.inmovement and self.path) or (self.inmovement and self.target):
            self.rot = (self.target - self.pos).angle_to(vec(1, 0))
            self.vel = vec(settings.PLAYER_SPEED, 0).rotate(-self.rot)

        elif self.inmovement:
            if abs(self.rot - (self.target - self.pos).angle_to(vec(1, 0))) < 1:
                self.rot = (self.target - self.pos).angle_to(vec(1, 0))
            self.vel = vec(settings.PLAYER_SPEED, 0).rotate(-self.rot)
