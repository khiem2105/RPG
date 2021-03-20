"""This file manage the map and the camera"""
import pygame as pg
import settings


class Map:
    """Map class"""

    def __init__(self, filename):
        """init variable"""
        self.data = []
        self.edata = []
        self.line_length = []
        self.offset = 0
        self.filename = filename
        self.tilewidth = 0
        with open(filename, "rt") as f:
            for line in f:
                if line[0] != "m" and line[0] != "l":
                    self.offset += len(line) + 1
                    self.line_length.append(len(line) + 1)
                    self.edata.append(line.strip())
                    if any(v != "0" for v in line.strip()):
                        self.tilewidth = max(self.tilewidth, len(line) - 1)
                        self.data.append(line.strip())
        self.tileheight = len(self.data)
        self.width = self.tilewidth * settings.TILESIZE
        self.height = self.tileheight * settings.TILESIZE


class Camera:
    """Camera class"""

    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0

    def apply(self, entity):
        """move the rect in relation to camera position"""
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        """update the camera"""
        self.x = -target.rect.centerx + int(settings.WIDTH / 2)
        self.y = -target.rect.centery + int(settings.HEIGHT / 2)
        # limit of scrolling
        self.x = min(0, self.x)  # left
        self.y = min(0, self.y)  # top
        self.x = max(-(self.width - settings.WIDTH) + 1, self.x)  # right
        self.y = max(-(self.height - settings.HEIGHT) + 1, self.y)
        self.camera = pg.Rect(self.x, self.y, self.width, self.height)

    def get_pos(self):
        """getter pos camera"""
        return (self.x, self.y)
