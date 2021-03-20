import pygame
import settings
import random
from os import path
from operator import sub
import copy
import draw

vec = pygame.math.Vector2

random.seed()

pygame.mixer.init()


def roll_the_dice(n, faces):
    """Simulation of a roll dice

    Args:
        n (int): Number of roll you want
        faces ([String): The number of faces of the dice

    Returns:
        int: the sum of the Roll the dice
    """
    return sum([random.randint(1, faces) for _ in range(n)])


class Spell(pygame.sprite.Sprite):
    def __init__(self, player):

        self.game_folder = path.dirname(__file__)
        self.img_folder = path.join(self.game_folder, "img")
        self.sound_folder = path.join(self.game_folder, "sound")
        self.groups = player.game.sprites[player.game.current_level]["A"]
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.pos = copy.copy(player.pos)
        self.player = player
        self.sound_effect = None
        player.spell = False
        self.game = player.game
        self.game.sprites[self.game.current_level]["S"].add(self)
        self.range = 0
        self.damage = 0
        self.myroll = roll_the_dice(1, 20)
        self.AOE = (0, 0)  # AOE effet in tiles (x/y)
        self.cd = 0  # CD IN TURNS
        self.effects = None
        self.manacost = 0
        self.level_acces = 0
        self.ttl = 0
        self.locked = False
        self.rot = 0
        self.rot_speed = 1500
        self.vel = vec(0, 0)
        self.target_pos = None
        self.passiv = None
        self.path = None
        self.sprite = None
        self.area_effet_ = None
        self.valid = False
        self.is_lauched = False
        self.image = pygame.Surface((settings.TILESIZE, settings.TILESIZE))
        self.size = (settings.TILESIZE, settings.TILESIZE)
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.icon = None
        self.sound_effet = None
        self.player.my_spell = None

    def choose_cible(self):
        """Check  in order to cast 1 spell per round and only on"""
        if self.is_valid():
            self.offensive_spell()
        else:
            self.kill()
            del self

    def cool_down_check(self):
        """Check if the cooldown of the spell is reset"""
        print(self.player.cool_down[self.name], self.player.turn)
        if self.player.cool_down[self.name] <= self.player.turn:
            self.player.is_casting = True
            self.player.spell_surface = self.player.draw_player_skill(self)
            self.choose_cible()
        else:
            self.kill()
            del self

    def set_velocity(self, entity):
        """Set the velocity depending of wich entity is locked with the spell usfull for sprites

        Args:
            entity (entity): entity were the spell is  going to be cast
        """
        try:
            self.vel = (
                vec(self.player.pos // settings.TILESIZE)
                - vec((entity.pos) // settings.TILESIZE)
            ) * 50
        except:
            self.vel = (
                vec(self.player.pos // settings.TILESIZE)
                - vec(
                    (entity.get_pos()[0]) // settings.TILESIZE,
                    entity.get_pos()[1] // settings.TILESIZE,
                )
            ) * 50

    def collide(self):
        return pygame.sprite.spritecollide(self, self.player.enemies, False)

    # Update sprite and animations

    def update(self):
        """Update function for sprite animation"""
        if self.type == "on_target":
            self.rot = (self.rot + self.rot_speed * self.game.tick) % 360
            self.pos += -self.vel * self.game.tick
            _ = pygame.transform.scale(pygame.image.load(self.path), self.size)
            self.image = pygame.transform.rotate(_, self.rot)
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            if (
                self.target_pos
                and (self.pos - self.target_pos).length() < settings.TILESIZE / 2
            ):
                self.player.spell_surface = self.player.draw_player_skill()
                draw.flush_aoe_area(self.game)
                self.kill()
                del self

        elif self.type == "conjuring_pop":
            self.pos = self.target_pos
            self.vel = (0, 0)
            self.rot = (self.rot + self.rot_speed * self.game.tick) % 360
            _ = pygame.transform.scale(
                pygame.image.load(self.path),
                (int(self.size[0] * 2), self.size[1] * 2),
            )
            self.image = pygame.transform.rotate(_, self.rot)
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            if self.rot > 350:
                self.player.spell_surface = self.player.draw_player_skill()
                draw.flush_aoe_area(self.game)
                self.kill()

        elif self.type == "on_player":
            self.rot = (self.rot + self.rot_speed * self.game.tick) % 360
            self.my_size[0] += 100 * self.game.tick
            self.my_size[1] += 100 * self.game.tick
            _ = pygame.transform.scale(
                pygame.image.load(self.path),
                (int(self.my_size[0]), int(self.my_size[1])),
            )
            self.image = pygame.transform.rotate(_, self.rot)
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            if self.my_size[0] >= 3 * self.AOE[0]:
                self.player.spell_surface = self.player.draw_player_skill()
                draw.flush_aoe_area(self.game)
                self.kill()
                del self
        elif self.type == "bonus":
            draw.flush_aoe_area(self.game)
            if (
                self.player.cool_down[self.__class__.__name__] <= self.player.turn
                and self.player.mana >= self.manacost
            ):
                draw.flush_aoe_area(self.game)
                if self.sound_effect:
                    self.sound_effet.play()
                if not self.passiv or (
                    self.passiv
                    and any(buff == self.passiv for buff in self.player.buff)
                ):

                    self.player.buff[self.__class__.__name__] = {}
                    # self.sound_effet.play()
                    for key in self.bonus:
                        if key != "PM":
                            self.player.dic_player[key] += self.bonus[key][0]
                        elif key == "PM":
                            settings.PM += self.bonus[key][0]
                        if self.passiv:
                            self.player.buff[self.__class__.__name__][
                                "passiv"
                            ] = self.passiv
                            self.player.buff[self.__class__.__name__][key] = (
                                key,
                                self.bonus[key][0],
                                self.player.turn + self.bonus[key][1],
                            )
                        else:
                            self.player.buff[self.__class__.__name__][key] = (
                                key,
                                self.bonus[key][0],
                                self.player.turn + self.bonus[key][1],
                            )
                        self.player.cool_down[self.__class__.__name__] = (
                            self.player.turn + self.cd
                        )
                        self.player.mana -= self.manacost
                        self.player.spell_surface = self.player.draw_player_skill()
                        self.game.log["log"].add_log(
                            "You gained + "
                            + str(self.bonus[key][0])
                            + " "
                            + str(key)
                            + " for "
                            + str(self.bonus[key][1])
                            + " turns"
                        )
                    self.kill()
                    del self

    # visual effect on y (always hit btw)

    def offensive_spell(self):
        """Main part of Spells
        2 case : on_target : You have to choose on cible in particular, you can hit multiples target if the AOE != (0,0)
                On_player : The spell is cast around the player !
        """
        self.player.my_spell = self
        while not self.locked:
            if self.locked == True:
                break
            for event in pygame.event.get():
                draw.draw(self.game)
                if event.type == pygame.KEYDOWN:
                    # If pressed key is ESC quit program
                    if event.key == pygame.K_BACKSPACE:
                        break
                if self.type == "on_target" or self.type == "conjuring_pop":
                    print("post on target")
                    draw.draw_aoe_area(self.game)
                    AOE_node = []
                    mouse_position = pygame.mouse.get_pos()
                    entity_node = [
                        enemy.get_current_position(self.game.current_level)
                        for enemy in self.player.game.enemy[self.game.current_level]
                    ]
                    mouse_node = self.game.grid[self.game.current_level][
                        int(
                            (mouse_position[1] - self.game.camera.get_pos()[1])
                            / settings.TILESIZE
                        )
                    ][
                        int(
                            (mouse_position[0] - self.game.camera.get_pos()[0])
                            / settings.TILESIZE
                        )
                    ]
                    if (
                        pygame.mouse.get_pressed()[0]
                        and not self.player.inmovement
                        and not any(
                            enemy.inmovement
                            for enemy in self.game.enemy[self.game.current_level]
                        )
                    ):
                        self.locked = True
                        # self.game.enemy[self.game.current_level]
                        if self.AOE != (0, 0):
                            # """ case if it's an AOE Spell"""
                            for row in self.game.grid[self.game.current_level]:
                                for node in row:

                                    t = map(sub, node.get_pos(), mouse_node.get_pos())

                                    test = tuple([abs(elt) for elt in t])
                                    if ((test[0]) <= self.AOE[0]) and (
                                        (test[1]) <= self.AOE[1]
                                    ):
                                        AOE_node.append(node)

                            target = [
                                enemy
                                for enemy in self.game.enemy[self.game.current_level]
                                if (
                                    enemy.get_current_position(self.game.current_level)
                                    == mouse_node
                                )
                            ]
                            target_bis = [
                                enemy
                                for enemy in self.game.enemy[self.game.current_level]
                                if (
                                    enemy.get_current_position(self.game.current_level)
                                    in AOE_node
                                )
                            ]
                            self.player.rot = (
                                mouse_node.get_pos() - self.player.pos
                            ).angle_to(vec(1, 0))
                            self.game.log["log"].add_log("You casted : " + self.name)

                            self.set_velocity(mouse_node)
                            self.target_pos = mouse_node.get_pos()
                            self.sound_effet.play()

                            if (
                                self.player.get_current_position(
                                    self.game.current_level
                                )
                                in AOE_node
                            ):
                                self.game.log["log"].add_log(
                                    "You hit Yourself with : "
                                    + self.__class__.__name__
                                    + " you took "
                                    + str(self.damage)
                                    + " damage"
                                )
                                self.player.health -= self.damage

                            for enemy in target_bis:
                                self.set_velocity(mouse_node)

                                enemy.take_dmg(self.damage)
                                self.game.log["log"].add_log(
                                    "You did " + str(self.damage) + " damage"
                                )

                                if not enemy.health:
                                    # have to do with combat log["log"]
                                    self.game.log["log"].add_log("Zombie is dead")
                                else:
                                    self.game.log["log"].add_log(
                                        str(enemy.__class__.__name__)
                                        + " has now a health of :"
                                        + str(enemy.health)
                                    )
                            self.player.is_casting = False
                            self.player.spell_surface = self.player.draw_player_skill()
                            self.player.mana -= self.manacost
                            self.player.cool_down[self.__class__.__name__] = (
                                self.player.turn + self.cd
                            )
                            return

                        else:
                            # """Case is it's spell without AOE """
                            if self.player.turn and mouse_node in entity_node:
                                self.player.is_casting = False
                                self.player.spell_surface = (
                                    self.player.draw_player_skill()
                                )
                                self.player.mana -= self.manacost
                                target = [
                                    enemy
                                    for enemy in self.game.enemy[
                                        self.game.current_level
                                    ]
                                    if (
                                        enemy.get_current_position(
                                            self.game.current_level
                                        )
                                        == mouse_node
                                    )
                                ]
                                self.target_pos = entity_node[
                                    entity_node.index(mouse_node)
                                ].get_pos()
                                self.player.rot = (
                                    self.target_pos - self.player.pos
                                ).angle_to(vec(1, 0))
                                self.game.log["log"].add_log(
                                    "You casted an offensive spell on a enemy"
                                )
                                self.rot = (
                                    (self.target_pos - self.pos).angle_to(vec(1, 0))
                                    - 90
                                ) % 360

                                for enemy in target:
                                    self.set_velocity(enemy)
                                    enemy.take_dmg(self.damage)
                                    self.game.log["log"].add_log(
                                        "You did " + str(self.damage) + " damage"
                                    )
                                    self.sound_effet.play()

                                    if not enemy.health:
                                        self.game.log["log"].add_log("Zombie is dead")
                                    else:
                                        self.game.log["log"].add_log(
                                            "Zombie has now a health of : "
                                            + str(enemy.health)
                                        )
                                draw.flush_aoe_area(self.game)
                                return

                            else:
                                self.player.is_casting = False
                                self.player.cool_down[self.__class__.__name__] = (
                                    self.player.turn + self.cd
                                )
                                self.player.mana -= self.manacost
                                self.player.spell_surface = (
                                    self.player.draw_player_skill()
                                )

                                draw.flush_aoe_area(self.game)

                                self.kill()
                        draw.flush_aoe_area(self.game)

                        return

                elif self.type == "on_player":
                    print("on_player oskour gang")
                    draw.flush_aoe_area(self.game)
                    self.locked = True
                    mouse_position = pygame.mouse.get_pos()
                    player_pos = self.player.get_current_position(
                        self.game.current_level
                    )
                    entity_node = [
                        enemy.get_current_position(self.game.current_level)
                        for enemy in self.player.game.enemy[self.game.current_level]
                    ]
                    mouse_node = self.game.grid[self.game.current_level][
                        int(
                            (mouse_position[1] - self.game.camera.get_pos()[1])
                            / settings.TILESIZE
                        )
                    ][
                        int(
                            (mouse_position[0] - self.game.camera.get_pos()[0])
                            / settings.TILESIZE
                        )
                    ]
                    AOE_node = []
                    self.sound_effet.play()

                    for row in self.game.grid[self.game.current_level]:
                        for node in row:
                            t = map(
                                sub,
                                node.get_pos(),
                                self.player.get_current_position(
                                    self.game.current_level
                                ).get_pos(),
                            )
                            if tuple([abs(elt) for elt in t]) <= self.AOE:
                                AOE_node.append(node)

                    self.game.log["log"].add_log(
                        "You casted an offensive spell on a enemy"
                    )
                    target_bis = [
                        enemy
                        for enemy in self.game.enemy[self.game.current_level]
                        if (
                            enemy.get_current_position(self.game.current_level)
                            in AOE_node
                        )
                    ]
                    print("target bis :", target_bis)
                    for enemy in target_bis:
                        self.player.cool_down[self.__class__.__name__] = (
                            self.player.turn + self.cd
                        )
                        enemy.take_dmg(self.damage)

                        if not enemy.health:
                            self.game.log["log"].add_log("Enemy is dead")
                        else:
                            self.game.log["log"].add_log(
                                "Enemy has now a health of : " + str(enemy.health)
                            )

                    draw.flush_aoe_area(self.game)
                    self.player.is_casting = False
                    self.player.spell_surface = self.player.draw_player_skill()
                    return
                    # TO DO

    def is_valid(self):
        """[Do a roll 20 in order to check if you can cast your spell

        Returns:
            boolean: Return True if randint(1,20) < player.int
        """
        if self.manacost <= self.player.mana:
            if self.myroll <= self.player.dic_player["Int"]:
                self.game.log["log"].add_log(
                    "You did a roll of "
                    + str(self.myroll)
                    + " : You can cast your spell"
                )
                return True
            else:
                self.game.log["log"].add_log(
                    "You failed you ROLL20 : [" + str(self.myroll) + "]"
                )
                self.player.is_casting = False
                self.player.cool_down[self.__class__.__name__] = (
                    self.player.turn + self.cd
                )
                self.player.spell_surface = self.player.draw_player_skill()
                self.kill()
                del self

                return False
        else:
            self.game.log["log"].add_log("Not enough mana")
            return False


##########################################################################################
# Sorcerer spells
##########################################################################################
class FireBall(Spell):
    def __init__(self, player, get_value=False):
        if not get_value:
            super().__init__(player)
        self.manacost = 20
        self.cd = 1
        self.icon_path = path.join(player.game.img_folder, "fireball_icon.png")
        self.AOE = (50, 50)
        if not get_value:
            self.range = settings.PM
            self.name = self.__class__.__name__
            # géré les dégats selon le wisdom et mettre un peu de ramdom a chaque fois qu'on fait
            # Normalement selon la wisdom mais pas encore possible
            self.damage = roll_the_dice(10, 6)

            self.ttl = 10

            self.AOE = (50, 50)
            self.size = self.AOE
            self.type = "on_target"
            self.path = path.join(self.img_folder, "fireball.png")
            self.image = pygame.transform.scale(
                pygame.image.load(self.path), (self.AOE)
            )
            self.icon_path = path.join(self.img_folder, "fireball_icon.png")
            self.icon = pygame.transform.scale(
                pygame.image.load(self.icon_path), (32, 32)
            )
            # une fireball*
            try:
                self.sound_effet = pygame.mixer.Sound(
                    path.join(self.sound_folder, "fireball_effect.ogg")
                )
            except:
                self.sound_effet = pygame.mixer.Sound(
                    path.join(self.sound_folder, "fireball_effect.mp3")
                )
            self.sound_effet.set_volume(0.025)

            self.cool_down_check()


class Acid_Arrow(Spell):
    def __init__(self, player, get_value=False):
        if not get_value:
            super().__init__(player)
        self.manacost = 20
        self.cd = 1
        if not get_value:
            self.range = settings.PM * 3 / 4
            self.damage = roll_the_dice(6, 4)
            self.name = self.__class__.__name__
            self.image = pygame.transform.scale(
                pygame.image.load(path.join(self.img_folder, "acid_arrow_icon.png")),
                (36, 36),
            )

            self.rot_speed = 0
            self.ttl = 10

            self.type = "on_target"
            self.path = path.join(self.img_folder, "Acid-Arrow.png")
            self.image = pygame.transform.scale(pygame.image.load(self.path), (36, 36))

            self.icon_path = path.join(self.img_folder, "acid_arrow_icon.png")
            self.icon = pygame.transform.scale(
                pygame.image.load(self.icon_path), (32, 32)
            )
            try:
                self.sound_effet = pygame.mixer.Sound(
                    path.join(self.sound_folder, "Acid_Arrow_effect.ogg")
                )
            except:
                self.sound_effet = pygame.mixer.Sound(
                    path.join(self.sound_folder, "Acid_Arrow_effect.mp3")
                )
            self.sound_effet.set_volume(0.025)
            self.cool_down_check()
        self.icon_path = path.join(player.game.img_folder, "acid_arrow_icon.png")


class Ray_of_Frost(Spell):
    def __init__(self, player, get_value=False):
        if not get_value:
            super().__init__(player)
        self.cd = 1
        self.manacost = 20
        if not get_value:
            super().__init__(player)
            self.range = settings.PM
            self.damage = roll_the_dice(8, 4)
            self.name = self.__class__.__name__
            self.path = path.join(self.img_folder, "ray_of_frost.png")
            self.image = pygame.transform.scale(pygame.image.load(self.path), (36, 36))

            self.icon_path = path.join(self.img_folder, "acid_arrow_icon.png")
            self.icon = pygame.transform.scale(
                pygame.image.load(self.icon_path), (32, 32)
            )

            self.ttl = 10
            self.type = "on_target"
            try:
                self.sound_effet = pygame.mixer.Sound(
                    path.join(self.sound_folder, "ray_of_frost_effect.ogg")
                )
            except:
                self.sound_effet = pygame.mixer.Sound(
                    path.join(self.sound_folder, "ray_of_frost_effect.mp3")
                )
            self.sound_effet.set_volume(0.025)
            self.cool_down_check()
            self.game.log["log"].add_log("cast a ray of frost")
        self.icon_path = path.join(player.game.img_folder, "ray_of_frost_icon.png")

    def hit_effect(self, entity):
        entity.PM = entity.PM - 20


class Circle_of_death(Spell):
    def __init__(self, player, get_value=False):
        if not get_value:
            super().__init__(player)
        self.cd = 1
        self.manacost = 20
        self.type = "on_player"
        if not get_value:
            self.range = 300
            self.damage = roll_the_dice(8, 6)
            self.name = self.__class__.__name__
            self.AOE = (50, 50)
            self.ttl = 10
            self.type = "on_player"
            self.my_size = list(self.size)
            self.path = path.join(self.img_folder, "Circle_of_Death.png")
            self.image = pygame.transform.scale(pygame.image.load(self.path), (36, 36))

            self.icon_path = path.join(self.img_folder, "Circle_of_death_icon.png")
            self.icon = pygame.transform.scale(
                pygame.image.load(self.icon_path), (32, 32)
            )

            try:
                self.sound_effet = pygame.mixer.Sound(
                    path.join(self.sound_folder, "Circle_of_Death_effect.ogg")
                )
            except:
                self.sound_effet = pygame.mixer.Sound(
                    path.join(self.sound_folder, "Circle_of_Death_effect.mp3")
                )

            self.sound_effet.set_volume(0.025)

            self.cool_down_check()
        self.icon_path = path.join(player.game.img_folder, "Circle_of_Death.png")


##########################################################################################
# BARBARIAN SPELL


##########################################################################################
class Armor_bump(Spell):
    def __init__(self, player, get_value=False):
        if not get_value:
            super().__init__(player)
        self.cd = 1
        self.manacost = 20
        if not get_value:
            self.range = 32
            self.damage = roll_the_dice(1, 6) + player.dic_player["armor"]
            self.name = self.__class__.__name__
            self.AOE = (36, 36)
            self.ttl = 10
            self.type = "on_player"
            self.path = path.join(self.img_folder, "ray_of_frost.png")
            self.image = pygame.transform.scale(pygame.image.load(self.path), (36, 36))

            self.icon_path = path.join(self.img_folder, "armor_bump_icon.png")
            self.icon = pygame.transform.scale(
                pygame.image.load(self.icon_path), (32, 32)
            )
            self.sound_effet = pygame.mixer.Sound(
                path.join(self.sound_folder, "Circle_of_Death_effect.ogg")
            )
            self.sound_effet.set_volume(0.025)

            self.cool_down_check()
        self.icon_path = path.join(player.game.img_folder, "armor_bump_icon.png")

        self.icon_path = path.join(player.game.img_folder, "Lighing_strike_icon.png")


class Berserker_Rage(Spell):
    def __init__(self, player, get_value=False):
        if not get_value:
            super().__init__(player)
        self.cd = 8
        self.manacost = 0
        if not get_value:
            self.type = "bonus"
            self.bonus = {"Str": (4, 4), "Con": (4, 4)}
            try:
                self.sound_effet = pygame.mixer.Sound(
                    path.join(self.sound_folder, "rage_effect.ogg")
                )
            except:
                self.sound_effet = pygame.mixer.Sound(
                    path.join(self.sound_folder, "rage_effect.mp3")
                )
                self.sound_effet.set_volume(0.025)
            self.sound_effet.play()
        self.icon_path = path.join(player.game.img_folder, "rage.jpg")


class Fast_Movement(Spell):
    def __init__(self, player, get_value=False):
        if not get_value:
            super().__init__(player)
        self.cd = 8
        self.manacost = 0
        if not get_value:
            self.passiv = "Berserker_Rage"
            self.type = "bonus"
            self.bonus = {"PM": (2 * settings.TILESIZE, 4)}
            self.sound_effet = None
        self.icon_path = path.join(player.game.img_folder, "fast_movement.jpg")


class Totem_Animal(Spell):
    def __init__(self, player, get_value=False):
        if not get_value:
            super().__init__(player)
        self.cd = 8
        self.manacost = 0
        if not get_value:
            self.passiv = "Berserker_Rage"
            self.type = "bonus"
            self.bonus = {"armor": (1, 4)}
            self.sound_effet = None
        self.icon_path = path.join(player.game.img_folder, "Totem_animal.jpg")


##########################################################################################
# ROGUES SPELLS#
##########################################################################################


class Feline_aspect(Spell):
    def __init__(self, player, get_value=False):
        if not get_value:
            super().__init__(player)
        self.cd = 4
        self.manacost = 30

        if not get_value:
            self.type = "bonus"
            self.bonus = {"Dex": (4, self.player.dic_player["level"] + 2)}
            try:
                self.sound_effet = pygame.mixer.Sound(
                    path.join(self.sound_folder, "rage_effect.ogg")
                )
            except:
                self.sound_effet = pygame.mixer.Sound(
                    path.join(self.sound_folder, "rage_effect.mp3")
                )
                self.sound_effet.set_volume(0.025)
                self.sound_effet.play()

        self.icon_path = path.join(player.game.img_folder, "feline_aspect.jpg")


class Call_of_stones(Spell):
    def __init__(self, player, get_value=False):
        if not get_value:
            super().__init__(player)
        self.manacost = 20
        self.cd = 1
        self.rot = 0
        self.rot_speed = 500
        self.icon_path = path.join(player.game.img_folder, "call_of_stone_icon.jpg")
        if not get_value:

            self.name = self.__class__.__name__
            # géré les dégats selon le wisdom et mettre un peu de ramdom a chaque fois qu'on fait
            # Normalement selon la wisdom mais pas encore possible
            self.damage = roll_the_dice(2, 6)

            self.ttl = 10
            self.AOE = (50, 50)
            self.size = self.AOE
            self.type = "conjuring_pop"
            self.path = path.join(player.game.img_folder, "call_of_stone.png")
            self.image = pygame.transform.scale(
                pygame.image.load(self.path), (self.AOE)
            )
            self.icon_path = path.join(player.game.img_folder, "call_of_stone_icon.jpg")
            self.icon = pygame.transform.scale(
                pygame.image.load(self.icon_path), (32, 32)
            )
            # une fireball*
            try:
                self.sound_effet = pygame.mixer.Sound(
                    path.join(self.sound_folder, "call_of_stone_effect.ogg")
                )
            except:
                self.sound_effet = pygame.mixer.Sound(
                    path.join(self.sound_folder, "call_of_stone_effect.mp3")
                )
            self.sound_effet.set_volume(0.025)

            self.cool_down_check()


class Lighting_Strike(Spell):
    def __init__(self, player, get_value=False):
        if not get_value:
            super().__init__(player)
        self.cd = 1
        self.manacost = 20
        self.icon_path = path.join(player.game.img_folder, "Lighing_strike_icon.png")
        self.path = path.join(player.game.img_folder, "Lighing_strike.png")
        if not get_value:
            self.range = 32
            self.damage = roll_the_dice(3, 6)
            self.name = self.__class__.__name__
            self.AOE = (0, 0)
            self.ttl = 10
            self.type = "on_target"
            self.image = pygame.transform.scale(pygame.image.load(self.path), (36, 36))

            self.icon_path = path.join(
                player.game.img_folder, "Lighing_strike_icon.png"
            )
            self.icon = pygame.transform.scale(
                pygame.image.load(self.icon_path), (32, 32)
            )
            try:
                self.sound_effet = pygame.mixer.Sound(
                    path.join(self.sound_folder, "lightning_strike_effect.ogg")
                )
            except:
                self.sound_effet = pygame.mixer.Sound(
                    path.join(self.sound_folder, "lightning_strike_effect.mp3")
                )

            self.sound_effet.set_volume(0.025)

            self.cool_down_check()
