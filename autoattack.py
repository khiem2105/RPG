"""module that contains Auto_attack class"""
from os import path
import copy
import pygame as pg
import settings

vec = pg.math.Vector2

pg.mixer.init()


class AutoAttack(pg.sprite.Sprite):
    """Class that manages the auto attack animation"""

    def __init__(self, player, target_pos):
        self.game_folder = path.dirname(__file__)
        self.pos = copy.copy(player.pos)
        self.target_pos = target_pos
        self.img_folder = path.join(self.game_folder, "img")
        self.sound_folder = path.join(self.game_folder, "sound")
        self.player = player
        self.game = self.player.game
        self.groups = player.game.sprites[player.game.current_level]["A"]
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game.sprites[self.game.current_level]["S"].add(self)
        self.image = pg.Surface((settings.TILESIZE, settings.TILESIZE))
        self.size = (settings.TILESIZE, settings.TILESIZE)
        self.rect = self.image.get_rect()
        self.sound_effet = None
        self.name = None
        self.vel = 0
        self.rot = None

    def update(self):
        """
        Update method of the animation.
        it manages it velocity.
        """
        if self.name == "RogueAttack":
            self.rot = ((self.target_pos - self.pos).angle_to(vec(1, 0)) + 135) % 360
            self.pos += (-self.vel) * self.game.tick
            _ = pg.transform.scale(pg.image.load(self.path), self.size)
            self.image = pg.transform.rotate(_, self.rot)
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            if (
                self.target_pos
                and (self.pos - self.target_pos).length() < settings.TILESIZE / 2
            ):
                self.kill()
        else:
            self.pos = self.player.pos - (self.player.pos - self.target_pos) / 2

            self.rot = (self.rot + 300 * self.game.tick) % 360
            _ = pg.transform.scale(pg.image.load(self.path), self.size)
            self.image = pg.transform.rotate(_, self.rot)
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            if abs(self.init_rot - self.rot) > 90:
                self.kill()


class RogueAttack(AutoAttack):
    """Rogue auto attack animation"""

    def __init__(self, player, target_pos):
        super().__init__(player, target_pos)

        try:
            self.sound_effet = pg.mixer.Sound(
                path.join(self.sound_folder, "Rogue_attack_effect.ogg")
            )
        except pg.error:
            self.sound_effet = pg.mixer.Sound(
                path.join(self.sound_folder, "Rogue_attack_effect.mp3")
            )
        self.sound_effet.play()
        self.sound_effet.set_volume(0.075)

        self.path = path.join(self.img_folder, "ScoutShortBow.png")
        self.image = pg.transform.scale(
            pg.image.load(self.path), (settings.TILESIZE, settings.TILESIZE)
        )

        self.vel = (
            vec(self.player.pos // settings.TILESIZE)
            - vec((target_pos) // settings.TILESIZE)
        ) * 100

        self.rot = ((self.target_pos - self.pos).angle_to(vec(1, 0)) + 135) % 360

        self.rot_speed = 0
        self.name = self.__class__.__name__


class BarbarianAttack(AutoAttack):
    """Barbarian auto attack animation"""

    def __init__(self, player, target_pos):
        super().__init__(player, target_pos)

        try:
            self.sound_effet = pg.mixer.Sound(
                path.join(self.sound_folder, "auto_babarian_effect.ogg")
            )
        except pg.error:
            self.sound_effet = pg.mixer.Sound(
                path.join(self.sound_folder, "auto_babarian_effect.mp3")
            )

        self.path = path.join(self.img_folder, "golden_sword.png")
        self.image = pg.transform.scale(
            pg.image.load(self.path), (settings.TILESIZE, settings.TILESIZE)
        )
        self.sound_effet.play()
        self.sound_effet.set_volume(0.075)
        self.init_rot = ((self.target_pos - self.pos).angle_to(vec(1, 0)) - 90) % 360
        self.rot = ((self.target_pos - self.pos).angle_to(vec(1, 0)) - 90) % 360
        self.rot_speed = 58
        self.name = self.__class__.__name__


class WizardAttack(AutoAttack):
    """Wizard auto attack animation"""

    def __init__(self, player, target_pos):
        super().__init__(player, target_pos)

        try:
            self.sound_effet = pg.mixer.Sound(
                path.join(self.sound_folder, "auto_wizard_effect.ogg")
            )
        except pg.error:
            self.sound_effet = pg.mixer.Sound(
                path.join(self.sound_folder, "auto_wizard_effect.mp3")
            )

        self.path = path.join(self.img_folder, "wizard_staff.png")
        self.image = pg.transform.scale(
            pg.image.load(self.path), (settings.TILESIZE, settings.TILESIZE)
        )
        self.sound_effet.play()
        self.sound_effet.set_volume(0.075)
        self.init_rot = ((self.target_pos - self.pos).angle_to(vec(1, 0)) - 90) % 360
        self.rot = ((self.target_pos - self.pos).angle_to(vec(1, 0)) - 90) % 360
        self.rot_speed = 58
        self.name = self.__class__.__name__
