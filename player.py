"""This file define the player and his actions"""
import pygame as pg
from entity import Entity
import settings
from os import path
from inventory import Inventory, Item
from random import randint
from tiledmap import Map, Camera
import player_sheet
import spell
from autoattack import RogueAttack, BarbarianAttack, WizardAttack

vec = pg.math.Vector2


class Player(Entity):
    """class player"""

    def __init__(self, game, x, y, dic=None, dic_inv=None, chara_dic=None):
        """initialise all the variables that the player will need"""
        super().__init__(game, x, y)
        self.reachables = {self.game.current_level: []}
        self.pm = settings.PM
        self.turn_text = pg.font.SysFont("Cascadia code", 40).render(
            "Turn : " + str(self.turn), True, settings.WHITE
        )
        self.outline = pg.font.SysFont("Cascadia code", 40).render(
            "Turn : " + str(self.turn), True, settings.BLACK
        )
        self.dic_player = None
        if chara_dic:
            self.dic_player = chara_dic["dic"]
        elif dic:
            self.dic_player = dic["dic"]
        self.dic_inv = dic_inv

        self.level_text = pg.font.SysFont("Cascadia code", 40).render(
            " Level : " + str(1), True, settings.WHITE
        )
        self.outline_level = pg.font.SysFont("Cascadia code", 40).render(
            " Level : " + str(1), True, settings.BLACK
        )
        self.cool_down = {
            "FireBall": 0,
            "Ray_of_Frost": 0,
            "Acid_Arrow": 0,
            "Circle_of_death": 0,
            "Berserker_Rage": 0,
            "Fast_Movement": 0,
            "Totem_Animal": 0,
            "Feline_aspect": 0,
            "Call_of_stones": 0,
            "Lighting_Strike": 0,
        }
        self.spell = True
        self.stealth = False
        if chara_dic:
            self.self_class = chara_dic["dic"]["class"]
        else:
            self.self_class = "Barbarian"
        self.quest = {}
        self.can_attack = True
        self.enemies = []
        self.dex = 13
        self.buff = {}
        self.attribute_point = 0
        self.incombat = False
        self.is_casting = False
        self.my_spell = None
        self.spell_info = {
            "Barbarian": {
                "spell1": {
                    "spell": spell.Berserker_Rage,
                    "image": pg.transform.scale(
                        pg.image.load(spell.Berserker_Rage(self, True).icon_path),
                        (
                            int(1.5 * settings.TILESIZE),
                            int(1.5 * settings.TILESIZE),
                        ),
                    ).convert_alpha(),
                    "manacost": spell.Berserker_Rage(self, True).manacost,
                    "cd": spell.Berserker_Rage(self, True).cd,
                },
                "spell2": {
                    "spell": spell.Fast_Movement,
                    "image": pg.transform.scale(
                        pg.image.load(spell.Fast_Movement(self, True).icon_path),
                        (
                            int(1.5 * settings.TILESIZE),
                            int(1.5 * settings.TILESIZE),
                        ),
                    ).convert_alpha(),
                    "manacost": spell.Fast_Movement(self, True).manacost,
                    "cd": spell.Fast_Movement(self, True).cd,
                },
                "spell3": {
                    "spell": spell.Totem_Animal,
                    "image": pg.transform.scale(
                        pg.image.load(spell.Totem_Animal(self, True).icon_path),
                        (
                            int(1.5 * settings.TILESIZE),
                            int(1.5 * settings.TILESIZE),
                        ),
                    ).convert_alpha(),
                    "manacost": spell.Totem_Animal(self, True).manacost,
                    "cd": spell.Totem_Animal(self, True).cd,
                },
            },
            "Wizard": {
                "spell1": {
                    "spell": spell.FireBall,
                    "image": pg.transform.scale(
                        pg.image.load(spell.FireBall(self, True).icon_path),
                        (
                            int(1.5 * settings.TILESIZE),
                            int(1.5 * settings.TILESIZE),
                        ),
                    ).convert_alpha(),
                    "manacost": spell.FireBall(self, True).manacost,
                    "cd": spell.FireBall(self, True).cd,
                },
                "spell2": {
                    "spell": spell.Ray_of_Frost,
                    "image": pg.transform.scale(
                        pg.image.load(spell.Ray_of_Frost(self, True).icon_path),
                        (
                            int(1.5 * settings.TILESIZE),
                            int(1.5 * settings.TILESIZE),
                        ),
                    ).convert_alpha(),
                    "manacost": spell.Ray_of_Frost(self, True).manacost,
                    "cd": spell.Ray_of_Frost(self, True).cd,
                },
                "spell3": {
                    "spell": spell.Circle_of_death,
                    "image": pg.transform.scale(
                        pg.image.load(spell.Circle_of_death(self, True).icon_path),
                        (
                            int(1.5 * settings.TILESIZE),
                            int(1.5 * settings.TILESIZE),
                        ),
                    ).convert_alpha(),
                    "manacost": spell.Circle_of_death(self, True).manacost,
                    "cd": spell.Circle_of_death(self, True).cd,
                },
            },
            "Rogue": {
                "spell1": {
                    "spell": spell.Feline_aspect,
                    "image": pg.transform.scale(
                        pg.image.load(spell.Feline_aspect(self, True).icon_path),
                        (
                            int(1.5 * settings.TILESIZE),
                            int(1.5 * settings.TILESIZE),
                        ),
                    ).convert_alpha(),
                    "manacost": spell.Feline_aspect(self, True).manacost,
                    "cd": spell.Feline_aspect(self, True).cd,
                },
                "spell2": {
                    "spell": spell.Call_of_stones,
                    "image": pg.transform.scale(
                        pg.image.load(spell.Call_of_stones(self, True).icon_path),
                        (
                            int(1.5 * settings.TILESIZE),
                            int(1.5 * settings.TILESIZE),
                        ),
                    ).convert_alpha(),
                    "manacost": spell.Call_of_stones(self, True).manacost,
                    "cd": spell.Call_of_stones(self, True).cd,
                },
                "spell3": {
                    "spell": spell.Lighting_Strike,
                    "image": pg.transform.scale(
                        pg.image.load(spell.Lighting_Strike(self, True).icon_path),
                        (
                            int(1.5 * settings.TILESIZE),
                            int(1.5 * settings.TILESIZE),
                        ),
                    ).convert_alpha(),
                    "manacost": spell.Lighting_Strike(self, True).manacost,
                    "cd": spell.Lighting_Strike(self, True).cd,
                },
            },
        }

        self.spell_background = pg.image.load(
            path.join(self.game.img_folder, "spell_background.png")
        ).convert_alpha()
        if not game.editor:
            self.player_sheet = player_sheet.player_sheet(game.screen)
            self.player_sheet.dic_player = self.dic_player
            if chara_dic:
                self.player_sheet.portrayal = chara_dic["portrayal_name_img"]
            else:
                self.player_sheet.portrayal = None
            self.player_sheet.initialised = True
            if chara_dic:
                self.inventory = Inventory(self.game, self.dic_player)
                if "dic_Ab" in self.inventory.char.keys():
                    del self.inventory.char["dic_Ab"]
            else:
                self.inventory = Inventory(game, self.dic_player, self.dic_inv, 24)
            self.spell_surface = self.draw_player_skill()
        self.qcheck = False
        if chara_dic:
            self.player_sprite = chara_dic["dic"]["class"][:3]
        else:
            self.player_sprite = None
        if self.dic_player:
            self.health = self.dic_player["hp"] = self.dic_player["Con"] * 10
        if self.self_class == "Barbarian":
            self.mana = 0
        else:
            self.mana = self.dic_player["Int"] * 10

    def update(self):
        """Update the player entity"""
        if not self.game.editor:
            if self.health <= 0:
                print("dead")
                quit(self.game)
            self.check_quest()
            l = []
            for key in self.buff:
                for char in self.buff[key]:
                    if self.buff[key][char][2] == self.turn:
                        if char != "PM" and char != "Armor":
                            self.dic_player[self.buff[key][char][0]] -= self.buff[key][
                                char
                            ][1]

                        else:
                            settings.PM -= self.buff[key][char][1]
                        if key not in l:
                            l.append(key)
            for _ in l:
                del self.buff[_]

            if all(
                enemy.turn == self.turn
                for enemy in self.game.enemy[self.game.current_level]
            ):
                self.level_up()
                if self.inmovement:
                    self.game.focus = self
                if (
                    not self.inmovement
                    and not self.path
                    and not self.reachables[self.game.current_level]
                    and not any(
                        enem.path != [] or enem.inmovement
                        for enem in self.game.enemy[self.game.current_level]
                    )
                ):
                    self.reach_draw = True
                    self.game.focus = self
                if not self.inmovement and not any(
                    enem.path != [] or enem.inmovement
                    for enem in self.game.enemy[self.game.current_level]
                ):
                    self.game.focus = self
                self.move()
                try:
                    self.image = pg.transform.rotate(
                        self.game.img[self.game.player.player_sprite], self.rot
                    )
                except:
                    self.image = pg.transform.rotate(self.game.img["P"], self.rot)
                self.mask = pg.mask.from_surface(self.image)
                self.rect = self.image.get_rect()
                self.rect.center = self.pos
                pos_ = self.pos + self.vel * self.game.tick
                self.pos = vec(round(pos_[0]), round(pos_[1]))
                self.find_enemies()
                if self.enemies:
                    self.attack()
                if (
                    self.game.sprites[self.game.current_level]["Po"]
                    and self.get_current_position(self.game.current_level)
                    == self.game.sprites[self.game.current_level]["Po"]
                    .sprites()[0]
                    .node
                    and self.asmove
                    and not any(
                        enem.isseen for enem in self.game.enemy[self.game.current_level]
                    )
                ):
                    if self.stealth:
                        self.pm = settings.PM * (3 / 4)
                    else:
                        self.pm = settings.PM
                    self.path = []
                    self.vel = vec(0, 0)
                    self.turn += 1
                    self.update_name()
                    self.asmove = False
                    self.reach_draw = True
                    self.reachables[self.game.current_level] = []
                    self.inmovement = False
                    self.game.change_map()
                    return
                if (
                    self.game.sprites[self.game.current_level]["BP"]
                    and self.get_current_position(self.game.current_level)
                    == self.game.sprites[self.game.current_level]["BP"]
                    .sprites()[0]
                    .node
                    and self.game.current_level > 0
                    and self.asmove
                    and not any(
                        enem.isseen for enem in self.game.enemy[self.game.current_level]
                    )
                ):
                    if self.stealth:
                        self.pm = settings.PM * (3 / 4)
                    else:
                        self.pm = settings.PM
                    self.turn += 1
                    self.update_name()
                    self.path = []
                    self.asmove = False
                    self.vel = vec(0, 0)
                    self.reach_draw = True
                    self.game.current_level -= 1
                    self.game.m_current_level = self.game.current_level
                    self.inmovement = False
                    self.reachables[self.game.current_level] = []
                    self.pos = vec(
                        (self.game.portal_pos[self.game.current_level][0] + 0.5)
                        * settings.TILESIZE,
                        (self.game.portal_pos[self.game.current_level][1] + 0.5)
                        * settings.TILESIZE,
                    )
                    self.game.map = Map(
                        path.join(
                            self.game.map_folder,
                            self.game.path_[self.game.current_level],
                        )
                    )
                    self.game.camera = Camera(self.game.map.width, self.game.map.height)
                    self.game.first = True
                    self.game.camera.update(self.game.focus)
                    self.game.update()
                    return
        else:
            self.image = pg.transform.rotate(self.game.img["Bar"], self.rot)
            self.rect = self.image.get_rect()
            self.rect.center = self.pos

    def draw_player_skill(self, current_spell=None):
        skill_surf = pg.Surface((400, 100), pg.SRCALPHA, 32)
        skill_surf.blit(self.spell_background, (0, 0))
        for cpt, spellt in enumerate(self.spell_info[self.self_class]):
            spell_ = self.spell_info[self.self_class][spellt]
            _ = pg.font.SysFont("Cascadia code", 32).render(
                pg.key.name(self.game.bind["spell " + str(cpt + 1)]).upper(),
                True,
                (settings.WHITE),
            )
            skill_surf.blit(
                spell_["image"],
                (
                    92 + 1.5 * cpt * settings.TILESIZE * 1.5,
                    skill_surf.get_height() // 2 - settings.TILESIZE * 1.5 // 2,
                ),
            )
            if isinstance(current_spell, spell_["spell"]) or any(
                buff == spell_["spell"].__name__ for buff in self.buff
            ):

                temp = pg.Rect(
                    92 + 1.5 * cpt * settings.TILESIZE * 1.5 - 1,
                    skill_surf.get_height() // 2 - settings.TILESIZE * 1.5 // 2 - 1,
                    spell_["image"].get_rect().width + 1,
                    spell_["image"].get_rect().height + 1,
                )
                pg.draw.rect(skill_surf, (204, 153, 51), temp, 2)
            skill_surf.blit(
                _,
                (
                    92
                    + 1.5 * cpt * settings.TILESIZE * 1.5
                    + (1.5 * settings.TILESIZE) // 2
                    - _.get_rect().width // 2,
                    skill_surf.get_height() // 2 + settings.TILESIZE * 1.5 // 2 + 1,
                ),
            )
            if self.self_class == "Barbarian":
                _ = pg.font.SysFont("Cascadia code", 32).render(
                    str(spell_["manacost"]), True, (settings.RED)
                )
            else:
                _ = pg.font.SysFont("Cascadia code", 32).render(
                    str(spell_["manacost"]), True, (settings.BLUE)
                )
            skill_surf.blit(
                _,
                (
                    92
                    + 1.5 * cpt * settings.TILESIZE * 1.5
                    + (1.5 * settings.TILESIZE) // 2
                    - _.get_rect().width // 2,
                    skill_surf.get_height() // 2
                    - settings.TILESIZE * 1.5 // 2
                    - 1
                    - _.get_rect().height,
                ),
            )
            if self.cool_down[spell_["spell"].__name__] - self.turn > 0:
                tmp = pg.Surface(
                    (int(settings.TILESIZE * 1.5), int(settings.TILESIZE * 1.5)),
                    pg.SRCALPHA,
                    32,
                )
                tmp.fill(settings.GREY)
                tmp.set_alpha(200)
                skill_surf.blit(
                    tmp,
                    (
                        92 + 1.5 * cpt * settings.TILESIZE * 1.5,
                        skill_surf.get_height() // 2 - settings.TILESIZE * 1.5 // 2,
                    ),
                )
                _ = pg.font.SysFont("Cascadia code", 32).render(
                    str(self.cool_down[spell_["spell"].__name__] - self.turn),
                    True,
                    (204, 153, 51),
                )
                skill_surf.blit(
                    _,
                    (
                        92
                        + 1.5 * cpt * settings.TILESIZE * 1.5
                        + spell_["image"].get_rect().width // 2
                        - _.get_rect().width // 2,
                        skill_surf.get_height() // 2
                        - settings.TILESIZE * 1.5 // 2
                        + +spell_["image"].get_rect().height // 2
                        - _.get_rect().height // 2,
                    ),
                )

        return skill_surf

    def draw_player_turn(self, screen):
        x_pos = (
            screen.get_width() // 2
            - self.spell_surface.get_width() // 2
            - self.turn_text.get_width()
            - 30
        )
        y_pos = screen.get_height() - self.turn_text.get_height()
        for x in range(-1, 2):
            for y in range(-1, 2):
                screen.blit(self.outline, (x_pos + x, y_pos + y))

        screen.blit(self.turn_text, (x_pos, y_pos))

    def draw_player_level(self, screen):
        x_pos = screen.get_width() // 2 + self.spell_surface.get_width() // 2 + 25
        y_pos = screen.get_height() - self.turn_text.get_height()
        for x in range(-1, 2):
            for y in range(-1, 2):
                screen.blit(self.outline_level, (x_pos + x, y_pos + y))

        screen.blit(self.level_text, (x_pos, y_pos))

    def getstate(self):

        current_state = self.__dict__.copy()
        current_state.pop("image")
        current_state.pop("groups")
        current_state.pop("_Sprite__g")
        current_state.pop("reachables")
        current_state.pop("current_node")
        current_state.pop("game")
        current_state.pop("mask")
        current_state.pop("turn_text")
        current_state.pop("outline")
        current_state.pop("level_text")
        current_state.pop("outline_level")
        current_state.pop("enemies")
        current_state.pop("inventory")
        current_state.pop("my_spell")
        current_state.pop("spell_info")
        current_state.pop("spell_surface")
        current_state.pop("spell_background")
        current_state.pop("player_sheet")
        current_state.pop("stealth")
        current_state.pop("path")
        return current_state

    def update_name(self):
        self.turn_text = pg.font.SysFont("Cascadia code", 40).render(
            "Turn : " + str(self.turn), True, settings.WHITE
        )
        self.outline = pg.font.SysFont("Cascadia code", 40).render(
            "Turn : " + str(self.turn), True, settings.BLACK
        )
        self.level_text = pg.font.SysFont("Cascadia code", 40).render(
            " Level : " + str(self.dic_player["level"]), True, settings.WHITE
        )
        self.outline_level = pg.font.SysFont("Cascadia code", 40).render(
            " Level : " + str(self.dic_player["level"]), True, settings.BLACK
        )

    def find_enemies(self):
        self.enemies.clear()
        for enemy in self.game.enemy[self.game.current_level]:
            if (
                (
                    enemy.get_current_position(self.game.current_level).get_pos()
                    - self.pos
                ).length()
                <= 3.5 * settings.TILESIZE
            ) and self.self_class == "Rogue":
                self.enemies.append(enemy)

            if (
                enemy.get_current_position(self.game.current_level).get_pos() - self.pos
            ).length() <= 1.5 * settings.TILESIZE:
                self.enemies.append(enemy)

    def attack(self):
        if (
            pg.mouse.get_pressed()[2]
            and not self.inmovement
            and not any(
                enemy.inmovement for enemy in self.game.enemy[self.game.current_level]
            )
        ):
            mouse_position = pg.mouse.get_pos()
            entity_node = [
                enemy.get_current_position(self.game.current_level)
                for enemy in self.game.enemy[self.game.current_level]
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
            if mouse_node in entity_node:
                target = [
                    enemy
                    for enemy in self.enemies
                    if (
                        enemy.get_current_position(self.game.current_level)
                        == mouse_node
                    )
                ]
                target_pos = entity_node[entity_node.index(mouse_node)].get_pos()
                self.rot = (target_pos - self.pos).angle_to(vec(1, 0))
                self.image = pg.transform.rotate(
                    self.game.img[self.player_sprite], self.rot
                )
                if len(target) == 1 and not target[0].health and not target[0].looted:
                    target[0].loot()
                if self.can_attack:
                    self.can_attack = False
                    if self.stealth:
                        self.Stealth()
                    for enemy in target:
                        if not enemy.health:
                            break

                        if enemy.health > 0:
                            rng = randint(1, 20)
                            if self.dic_player["weapon"] > 0:
                                rand_weapon = randint(1, self.dic_player["weapon"])
                            else:
                                rand_weapon = 1
                            if rng == 1:
                                self.auto_attack(enemy)
                                self.game.log["log"].add_log(
                                    "Player : succesfull attack "
                                    + str(2 * (rand_weapon + self.dic_player["Str"]))
                                    + " (Weapon : "
                                    + str(2 * rand_weapon)
                                    + ", Strength : "
                                    + str(2 * self.dic_player["Str"])
                                    + ") damage inflicted to "
                                    + enemy.type_enemy
                                    + " ("
                                    + "roll of "
                                    + str(rng)
                                    + ")"
                                )
                                enemy.take_dmg(
                                    2 * (rand_weapon + self.dic_player["Str"])
                                )
                            elif rng <= self.dic_player["Str"]:
                                self.auto_attack(enemy)
                                self.game.log["log"].add_log(
                                    "Player : succesfull attack "
                                    + str(rand_weapon + self.dic_player["Str"])
                                    + "(Weapon : "
                                    + str(rand_weapon)
                                    + ", Strength : "
                                    + str(self.dic_player["Str"])
                                    + ") damage inflicted to "
                                    + enemy.type_enemy
                                    + " ("
                                    + "roll of "
                                    + str(rng)
                                    + ")"
                                )
                                enemy.take_dmg(rand_weapon + self.dic_player["Str"])
                            else:
                                self.game.log["log"].add_log(
                                    "Player : failed attack "
                                    + str(0)
                                    + " damage inflicted to "
                                    + enemy.type_enemy
                                    + " ("
                                    + "roll of "
                                    + str(rng)
                                    + ")"
                                )

    def auto_attack(self, enemy):
        if self.self_class == "Barbarian":
            BarbarianAttack(self.game.player, enemy.pos)
            self.mana = min(self.mana + 20, self.dic_player["Int"] * 10)
        elif self.self_class == "Wizard":
            WizardAttack(self.game.player, enemy.pos)
        elif self.self_class == "Rogue":
            RogueAttack(self.game.player, enemy.pos)

    def avoid_attack(self):
        rng = randint(1, 20)
        if rng <= self.dic_player["Dex"]:
            self.game.log["log"].add_log(
                "Player : Succeeded at avoid attack (" + "roll of " + str(rng) + ")"
            )
            return False
        self.game.log["log"].add_log(
            "Player : Failed at avoid attack (" + "roll of " + str(rng) + ")"
        )
        return True

    def update_inv(self):
        for key in self.inventory.char:
            self.dic_player[key] = self.inventory.char[key]

    def level_up(self):
        if self.dic_player and int(self.dic_player["xp"]) >= 100 * pow(
            2, self.dic_player["level"] - 1
        ):
            self.dic_player["xp"] -= 100 * pow(2, self.dic_player["level"] - 1)
            self.dic_player["level"] += 1
            self.dic_player["carac point"] += 1

    def check_quest(self):
        if self.qcheck:
            self.qcheck = False
            for item in self.inventory.liste:
                if item:
                    if item.item_id == 1000:
                        self.inventory.gold += item.stack
                        self.inventory.liste[self.inventory.liste.index(item)] = None
            for quest in self.quest:
                if (
                    self.game.quest.quest_list[str(quest)]["type"] == "0"
                    or self.game.quest.quest_list[str(quest)]["type"] == "2"
                ):
                    self.quest[quest] = 0
                    for item in self.inventory.liste:
                        if item:
                            if item.item_id == int(
                                self.game.quest.quest_list[str(quest)]["item"]
                            ):
                                self.quest[quest] = min(
                                    self.quest[quest] + item.stack,
                                    int(
                                        self.game.quest.quest_list[str(quest)][
                                            "objective"
                                        ]
                                    ),
                                )
                elif self.game.quest.quest_list[str(quest)]["type"] == "3":
                    self.quest[quest] = 0
                    for i in range(31, 43):
                        if Item(i, self.game.all_item) in self.inventory.liste:
                            self.quest[quest] = min(
                                self.quest[quest] + 1,
                                int(
                                    self.game.quest.quest_list[str(quest)]["objective"]
                                ),
                            )

        self.game.log["quest"].log_list = []
        for quest in self.quest:
            self.game.log["quest"].add_log(
                self.game.quest.quest_list[str(quest)]["name"], True
            )
            if self.game.quest.quest_list[str(quest)]["type"] == "0":
                self.game.log["quest"].add_log(
                    "- "
                    + Item(
                        int(self.game.quest.quest_list[str(quest)]["item"]),
                        self.game.all_item,
                    ).name
                    + " : "
                    + str(self.quest[quest])
                    + " / "
                    + self.game.quest.quest_list[str(quest)]["objective"]
                )
            elif self.game.quest.quest_list[str(quest)]["type"] == "1":
                self.game.log["quest"].add_log(
                    "- "
                    + self.game.quest.quest_list[str(quest)]["enemy"].capitalize()
                    + "  killed : "
                    + str(self.quest[quest])
                    + " / "
                    + self.game.quest.quest_list[str(quest)]["objective"]
                )
            elif self.game.quest.quest_list[str(quest)]["type"] == "2":
                self.game.log["quest"].add_log(
                    "- "
                    + Item(
                        int(self.game.quest.quest_list[str(quest)]["item"]),
                        self.game.all_item,
                    ).name
                    + " : "
                    + str(self.quest[quest])
                    + " / "
                    + self.game.quest.quest_list[str(quest)]["objective"]
                )
            elif self.game.quest.quest_list[str(quest)]["type"] == "3":
                self.game.log["quest"].add_log(
                    "- "
                    + "Pieces of parchment"
                    + " : "
                    + str(self.quest[quest])
                    + " / "
                    + self.game.quest.quest_list[str(quest)]["objective"]
                )
            self.game.log["quest"].add_log("")

    def Stealth(self):
        """
        Allow to activate/desactivate the stealth, and so, to change the pm value
        and update the current accessible area when the stealth is activated/desactivated
        """
        if not self.stealth:
            self.stealth = True
            self.pm *= 3 / 4
            self.reachables[self.game.current_level] = []
            self.reach_draw = True
        elif self.stealth:
            self.stealth = False
            self.pm *= 4 / 3
            self.reachables[self.game.current_level] = []
            self.reach_draw = True

    def draw_player_mana(self, surf, x, y, pct):
        if pct < 0:
            pct = 0
        elif pct > 1:
            pct = 1
        BAR_LENGTH = 20
        BAR_HEIGHT = 100
        fill = pct * BAR_HEIGHT
        outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pg.Rect(x, y - fill + BAR_HEIGHT, BAR_LENGTH, fill)
        text_surface = pg.font.SysFont("cascadia code", 20).render(
            str(self.mana), True, settings.WHITE
        )
        if self.self_class == "Barbarian":
            pg.draw.rect(surf, settings.RED, fill_rect)
        else:
            pg.draw.rect(surf, settings.BLUE, fill_rect)
        pg.draw.rect(surf, settings.WHITE, outline_rect, 1)
        surf.blit(
            text_surface,
            (
                x + BAR_LENGTH // 2 - text_surface.get_rect().width // 2,
                y - text_surface.get_rect().height,
            ),
        )

    def draw_player_health(self, surf, x, y, pct):
        if pct < 0:
            pct = 0
        elif pct > 1:
            pct = 1
        BAR_LENGTH = 20
        BAR_HEIGHT = 100
        fill = pct * BAR_HEIGHT
        outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pg.Rect(x, y - fill + BAR_HEIGHT, BAR_LENGTH, fill)
        text_surface = pg.font.SysFont("cascadia code", 20).render(
            str(self.health), True, settings.WHITE
        )
        if pct > 0.6:
            col = settings.GREEN
        elif pct > 0.3:
            col = settings.YELLOW
        else:
            col = settings.RED

        pg.draw.rect(surf, col, fill_rect)
        pg.draw.rect(surf, settings.WHITE, outline_rect, 1)
        surf.blit(
            text_surface,
            (
                x + BAR_LENGTH // 2 - text_surface.get_rect().width // 2,
                y - text_surface.get_rect().height,
            ),
        )

    def draw_xp_bar(self, surf, x, y, pct):
        if pct < 0:
            pct = 0
        elif pct > 1:
            pct = 1
        BAR_LENGTH = 400
        BAR_HEIGHT = 5
        fill = pct * BAR_LENGTH
        outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
        pg.draw.rect(surf, settings.ORANGE, fill_rect)
        pg.draw.rect(surf, settings.WHITE, outline_rect, 1)
        text_surface = pg.font.SysFont("cascadia code", 20).render(
            str(self.dic_player["xp"] / (pow(2, self.dic_player["level"] - 1))) + " %",
            True,
            settings.WHITE,
        )
        surf.blit(
            text_surface,
            (
                x + BAR_LENGTH // 2 - text_surface.get_rect().width // 2,
                y - text_surface.get_rect().height,
            ),
        )


def turn(self):

    if (
        not self.inmovement
        and not self.path
        and all(
            self.turn == enemy.turn and not enemy.path and not enemy.inmovement
            for enemy in self.game.enemy[self.game.current_level]
        )
        and all(
            pnj.talking == None
            for pnj in self.game.sprites[self.game.current_level]["M"]
        )
    ):
        for enem in self.game.enemy[self.game.current_level]:
            enem.path = []
        if self.pm == settings.PM and self.can_attack and self.spell:
            self.health = min(self.health + 20, self.dic_player["Con"] * 10)
            if self.self_class != "Barbarian":
                self.mana = min(self.mana + 10, self.dic_player["Int"] * 10)
            else:
                self.mana = max(0, self.mana - 10)
        self.path = []
        self.turn += 1
        self.spell = True
        self.can_attack = True
        if self.stealth:
            self.pm = settings.PM * (3 / 4)
        elif self.inventory.weight > self.inventory.get_volume(self.dic_player["Str"]):
            self.pm = settings.PM * (2 / 3)
        else:
            self.pm = settings.PM
        self.reachables[self.game.current_level] = []
        self.update_name()
        self.game.log["log"].add_log(
            "----------------TURN " + str(self.turn) + "-------------------"
        )
        self.spell_surface = self.draw_player_skill()
        for key in self.cool_down:
            if self.cool_down[key] < self.turn:
                self.cool_down[key] = self.turn
