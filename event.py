"""the main purpose of this file is to manage all the user interaction
that will modify the course of the game"""
from random import choice
from os import path
import math
import pygame as pg
from interaction_pnj_perso import acheter, vendre
from item import Item
from save import save, create_map
from pathfinding import astar, Node
from draw import draw_path, flush_path, flush_reachable, draw_aoe_area
import settings

from box import Button, Input
from player import turn
from enemy import Enemy
from spell import (
    FireBall,
    Ray_of_Frost,
    Circle_of_death,
    Berserker_Rage,
    Fast_Movement,
    Totem_Animal,
    Call_of_stones,
    Feline_aspect,
    Lighting_Strike,
)
from combat_log import Log
import math
from operator import sub

vec = pg.math.Vector2


def events(self):
    """this function catch all the event and deal with them."""
    spawn(self)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            self.quit()
        if event.type == pg.KEYDOWN and event.key == pg.K_c:
            self.player.Stealth()  # allow to activate/desactivate the stealth

        if (
            pg.key.get_pressed()[self.bind["map"]]
            and event.type == pg.KEYDOWN
            and not (self.shortcut or self.is_console_opened)
        ):
            self.mmap = not self.mmap

        if (
            pg.key.get_pressed()[self.bind["player 1"]]
            and event.type == pg.KEYDOWN
            and not (self.shortcut or self.mmap or self.is_console_opened)
        ):
            if self.player.self_class != "Wizard":
                change_player(self, "Wizard")
                self.player.spell_surface = self.player.draw_player_skill()

        if (
            pg.key.get_pressed()[self.bind["player 2"]]
            and event.type == pg.KEYDOWN
            and not (self.shortcut or self.mmap or self.is_console_opened)
        ):
            if self.player.self_class != "Barbarian":
                change_player(self, "Barbarian")
                self.player.spell_surface = self.player.draw_player_skill()
        if (
            pg.key.get_pressed()[self.bind["player 3"]]
            and event.type == pg.KEYDOWN
            and not (self.shortcut or self.mmap)
        ):
            if self.player.self_class != "Rogue":
                change_player(self, "Rogue")
                self.player.spell_surface = self.player.draw_player_skill()

        if (
            pg.key.get_pressed()[pg.K_ESCAPE]
            and event.type == pg.KEYDOWN
            and not (self.shortcut or self.mmap or self.is_console_opened)
        ):
            self.buttons.clear()
            for pnj in self.sprites[self.current_level]["J"]:
                pnj.talking = None
                pnj.talking_pos = None
                pnj.quest = False
                self.log["pnj"] = None
            for pnj in self.sprites[self.current_level]["M"]:
                pnj.talking = None
                pnj.talking_pos = None
                pnj.quest = False
                self.log["pnj"] = None
            self.pause = not self.pause
            if self.pause:
                pause(self)

        if (
            pg.key.get_pressed()[pg.K_TAB]
            and event.type == pg.KEYDOWN
            and not (self.shortcut or self.mmap or self.pause)
        ):
            for pnj in self.sprites[self.current_level]["J"]:
                pnj.talking = None
                pnj.talking_pos = None
                pnj.quest = False
                self.log["pnj"] = None
            for pnj in self.sprites[self.current_level]["M"]:
                pnj.talking = None
                pnj.talking_pos = None
                pnj.quest = False
                self.log["pnj"] = None
            self.is_console_opened = not self.is_console_opened
            if self.is_console_opened:
                console_menu(self)

        if self.is_console_opened:
            self.my_input.event(event)
            if pg.key.get_pressed()[pg.K_RETURN]:
                print("tololo")
                console(self.player, self.my_input.text)
                self.my_input.istyping = True

        if (
            pg.key.get_pressed()[self.bind["inventory"]]
            and event.type == pg.KEYDOWN
            and not (self.shortcut or self.mmap or self.is_console_opened)
        ):
            self.player.inventory.open()
            self.player.update_inv()

        if (
            pg.key.get_pressed()[self.bind["player sheet"]]
            and event.type == pg.KEYDOWN
            and not (self.shortcut or self.mmap or self.is_console_opened)
        ):
            self.player.player_sheet.open()

        if (
            not self.player.player_sheet.isActive
            and self.player.dic_player["carac point"] != 0
        ):
            for i, cara in enumerate(self.player.dic_player):
                if (
                    (2 <= i <= 7)
                    and cara != "spells"
                    and self.player.dic_player[cara] < 18
                ):
                    if self.player.player_sheet.list_button[cara].is_cliked(event):
                        self.player.dic_player[cara] += 1
                        self.player.dic_player["carac point"] -= 1
                        self.player.player_sheet.surf = self.player.player_sheet.draw()

        if self.pause:
            if (
                self.buttons["save & quit"].is_cliked(event)
                and not self.player.inmovement
            ):
                save(self, self.save_name)
                self.quit()
            elif self.buttons["shortcut"].is_cliked(event):
                self.buttons.clear()
                self.inputs.clear()
                self.pause = False
                self.shortcut = True
                shortcut(self)
            elif self.buttons["save"].is_cliked(event) and not self.player.inmovement:
                save(self, self.save_name)

        if self.shortcut:
            if pg.key.get_pressed()[pg.K_ESCAPE] and event.type == pg.KEYDOWN:
                self.shortcut = False
            else:
                for key in self.inputs:
                    self.inputs[key].event(event, True)
                    if event.type == pg.KEYDOWN and self.inputs[key].istyping:
                        self.bind[key] = event.key

        if self.mmap:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 4:
                if self.m_current_level < len(self.mmap_group) - 1:
                    self.m_current_level += 1

            if event.type == pg.MOUSEBUTTONDOWN and event.button == 5:
                if self.m_current_level > 0:
                    self.m_current_level -= 1
        if not self.mmap and not self.pause and not self.shortcut:
            self.log["log"].event(event)
            if self.buttons:
                if any(enemy.looting for enemy in self.enemy[self.current_level]):
                    self.buttons[0].ennemy[0].loot()
                    for key in self.buttons:
                        try:

                            iscolliding = self.buttons[key].rect.collidepoint(event.pos)
                            if iscolliding:
                                test = pg.Rect(
                                    12,
                                    30 + 30 * 2 * key,
                                    self.buttons[key].rect.width,
                                    self.buttons[key].rect.height,
                                )
                                pg.draw.rect(
                                    self.buttons[key].ennemy[0].looting,
                                    (0, 0, 0),
                                    test,
                                    2,
                                )
                        except AttributeError:
                            pass
                        if self.buttons[key].is_cliked(event):
                            if self.player.inventory.add_item(
                                self.buttons[key].ennemy[1].item_id,
                                self.buttons[key].ennemy[1].stack,
                            ):
                                self.buttons[key].ennemy[0].item.remove(
                                    self.buttons[key].ennemy[1]
                                )
                                self.buttons[key].ennemy[0].loot()
                                break
            liste_de_pnj = []
            for pnjM in self.sprites[self.current_level]["M"]:
                liste_de_pnj.append(pnjM)
            for pnjJ in self.sprites[self.current_level]["J"]:
                liste_de_pnj.append(pnjJ)
            for pnj in liste_de_pnj:
                if pnj.talking:
                    if pnj.quest:
                        if pnj.solving_quest:
                            self.log["pnj"].add_log(pnj.text["During quest"])
                        self.log["pnj"].event(event)
                        if pnj.has_quest["type_reward"] == "item":
                            item = Item(int(pnj.has_quest["reward"]), self.all_item)
                            game_folder = path.dirname(__file__)
                            img_folder = path.join(game_folder, "img")
                            img = pg.image.load(path.join(img_folder, item.img))
                        elif pnj.has_quest["type_reward"] == "money":
                            img = pg.font.SysFont("Garamond", 22).render(
                                pnj.has_quest["reward"], True, (204, 153, 51)
                            )
                        else:
                            break
                        pnj.talking.blit(
                            pg.image.load(path.join(self.img_folder, "loot.png")),
                            (0, 0),
                        )
                        pnj.talking.blit(
                            img,
                            (
                                self.log["pnj"].width // 2
                                + 5
                                - img.get_rect().width // 2,
                                self.log["pnj"].height + 40,
                            ),
                        )

                        _ = pg.font.SysFont("Garamond", 22).render(
                            "Accept", True, (204, 153, 51)
                        )
                        pnj.talking.blit(
                            _, (5, self.log["pnj"].height + 40 + img.get_height() + 10)
                        )
                        _ = pg.font.SysFont("Garamond", 22).render(
                            "Complete", True, (204, 153, 51)
                        )
                        pnj.talking.blit(
                            _,
                            (
                                pnj.talking.get_rect().width // 2,
                                self.log["pnj"].height + 40 + img.get_height() + 10,
                            ),
                        )

                        for cpt, key in enumerate(self.buttons):
                            try:
                                iscolliding = self.buttons[key].rect.collidepoint(
                                    event.pos
                                )
                                if iscolliding:
                                    test = pg.Rect(
                                        self.buttons[key].rect.x - pnj.talking_pos[0],
                                        self.buttons[key].rect.y - pnj.talking_pos[1],
                                        self.buttons[key].rect.width,
                                        self.buttons[key].rect.height,
                                    )
                                    pg.draw.rect(pnj.talking, (0, 0, 0), test, 2)
                            except AttributeError:
                                pass
                        if self.buttons["accept"].is_cliked(event):
                            if len(self.player.quest) <= 2:
                                if all(
                                    key != pnj.quest_id for key in self.player.quest
                                ):
                                    self.player.quest[pnj.quest_id] = 0
                                    self.player.qcheck = True
                                    self.player.inmovement = True
                                    pnj.solving_quest = True
                        elif self.buttons["complete"].is_cliked(event):
                            for key in self.player.quest:
                                if key == pnj.quest_id and self.player.quest[
                                    key
                                ] == int(pnj.has_quest["objective"]):
                                    self.log["pnj"].add_log(pnj.text["Fulfilled quest"])
                                    pnj.solving_quest = False
                                    del self.player.quest[key]
                                    if pnj.has_quest["type_reward"] == "item":
                                        self.player.inventory.add_item(
                                            int(pnj.has_quest["reward"])
                                        )
                                    elif pnj.has_quest["type_reward"] == "money":
                                        self.player.inventory.gold += int(
                                            pnj.has_quest["reward"]
                                        )
                                    pnj.quest = False
                                    pnj.has_quest = None
                                    self.player.inmovement = True
                                    return

                    elif not pnj.quest:
                        pnj.talk()
                        for cpt, key in enumerate(self.buttons):
                            try:
                                iscolliding = self.buttons[key].rect.collidepoint(
                                    event.pos
                                )
                                if iscolliding:
                                    test = pg.Rect(
                                        12,
                                        60 + 60 * cpt,
                                        self.buttons[key].rect.width,
                                        self.buttons[key].rect.height,
                                    )
                                    pg.draw.rect(pnj.talking, (0, 0, 0), test, 2)
                            except AttributeError:
                                pass
                        if pnj.is_merchant:
                            if self.buttons["buy"].is_cliked(event):
                                acheter(self, pnj.store, self.player.inventory)
                            elif self.buttons["sell"].is_cliked(event):
                                vendre(self, pnj.store, self.player.inventory)
                    if pnj.has_quest and not pnj.quest:
                        if self.buttons["quest"].is_cliked(event):
                            game_folder = path.dirname(__file__)
                            img_folder = path.join(game_folder, "img")
                            pnj.quest = True
                            self.buttons.clear()
                            self.log["pnj"] = Log(
                                pnj.talking.get_rect().width - 10,
                                pnj.talking.get_rect().height - 150,
                                (pnj.talking_pos[0] + 5, pnj.talking_pos[1] + 30),
                                settings.WHITE,
                                26,
                                self,
                                False,
                                True,
                            )
                            pnj.talking.blit(
                                pg.image.load(path.join(img_folder, "loot.png")), (0, 0)
                            )
                            self.log["pnj"].add_log(pnj.text["Before quest"])
                            if pnj.has_quest["type_reward"] == "item":
                                item = Item(int(pnj.has_quest["reward"]), self.all_item)
                                img = pg.image.load(path.join(img_folder, item.img))
                            elif pnj.has_quest["type_reward"] == "money":
                                img = pg.font.SysFont("Garamond", 22).render(
                                    pnj.has_quest["reward"], True, (204, 153, 51)
                                )
                            pnj.talking.blit(
                                img,
                                (
                                    self.log["pnj"].width // 2
                                    + 5
                                    - img.get_rect().width // 2,
                                    self.log["pnj"].height + 40,
                                ),
                            )
                            self.buttons["accept"] = Button(
                                pnj.talking_pos[0] + 5,
                                pnj.talking_pos[1]
                                + self.log["pnj"].height
                                + 40
                                + img.get_height()
                                + 10,
                                (
                                    pnj.talking.get_rect().width // 2 - 10,
                                    pg.font.SysFont("Garamond", 22).get_height(),
                                ),
                            )
                            _ = pg.font.SysFont("Garamond", 22).render(
                                "Accept", True, (204, 153, 51)
                            )
                            pnj.talking.blit(
                                _,
                                (
                                    5,
                                    self.log["pnj"].height + 40 + img.get_height() + 10,
                                ),
                            )
                            _ = pg.font.SysFont("Garamond", 22).render(
                                "Complete", True, (204, 153, 51)
                            )
                            pnj.talking.blit(
                                _,
                                (
                                    pnj.talking.get_rect().width // 2,
                                    self.log["pnj"].height + 40 + img.get_height() + 10,
                                ),
                            )
                            self.buttons["complete"] = Button(
                                pnj.talking_pos[0] + pnj.talking.get_rect().width // 2,
                                pnj.talking_pos[1]
                                + self.log["pnj"].height
                                + 40
                                + img.get_height()
                                + 10,
                                (
                                    pnj.talking.get_rect().width // 2,
                                    pg.font.SysFont("Garamond", 22).get_height(),
                                ),
                            )
                        else:
                            break
                        pnj.talking.blit(
                            img,
                            (
                                self.log["pnj"].width // 2
                                + 5
                                - img.get_rect().width // 2,
                                self.log["pnj"].height + 40,
                            ),
                        )
                        self.buttons["accept"] = Button(
                            pnj.talking_pos[0] + 5,
                            pnj.talking_pos[1]
                            + self.log["pnj"].height
                            + 40
                            + img.get_height()
                            + 10,
                            (
                                pnj.talking.get_rect().width // 2 - 10,
                                pg.font.SysFont("Garamond", 22).get_height(),
                            ),
                        )
                        _ = pg.font.SysFont("Garamond", 22).render(
                            "Accept", True, (204, 153, 51)
                        )
                        pnj.talking.blit(
                            _, (5, self.log["pnj"].height + 40 + img.get_height() + 10)
                        )
                        _ = pg.font.SysFont("Garamond", 22).render(
                            "Complete", True, (204, 153, 51)
                        )
                        pnj.talking.blit(
                            _,
                            (
                                pnj.talking.get_rect().width // 2,
                                self.log["pnj"].height + 40 + img.get_height() + 10,
                            ),
                        )
                        self.buttons["complete"] = Button(
                            pnj.talking_pos[0] + pnj.talking.get_rect().width // 2,
                            pnj.talking_pos[1]
                            + self.log["pnj"].height
                            + 40
                            + img.get_height()
                            + 10,
                            (
                                pnj.talking.get_rect().width // 2,
                                pg.font.SysFont("Garamond", 22).get_height(),
                            ),
                        )

            if pg.key.get_pressed()[self.bind["turn"]]:
                turn(self.player)

            if (
                pg.key.get_pressed()[self.bind["spell 1"]]
                and not self.player.inmovement
                and self.player.spell
                and not self.is_console_opened
                and not any(enem.inmovement for enem in self.enemy[self.current_level])
            ):
                if self.player.stealth:
                    self.player.Stealth()  # allow to desactivate the stealth if it is activated
                if self.player.self_class == "Barbarian":
                    Berserker_Rage(self.player)
                    Fast_Movement(self.player)
                    Totem_Animal(self.player)
                if self.player.self_class == "Rogue":
                    Feline_aspect(self.player)
                else:
                    FireBall(self.player)

            if (
                pg.key.get_pressed()[self.bind["spell 2"]]
                and not self.player.inmovement
                and self.player.spell
                and not self.is_console_opened
                and not any(enem.inmovement for enem in self.enemy[self.current_level])
            ):
                if self.player.stealth:
                    self.player.Stealth()

                if self.player.self_class == "Rogue":
                    Call_of_stones(self.player)
                if self.player.self_class == "Wizard":
                    Ray_of_Frost(self.player)

            if (
                pg.key.get_pressed()[self.bind["spell 3"]]
                and not self.player.inmovement
                and self.player.spell
                and not self.is_console_opened
                and not any(enem.inmovement for enem in self.enemy[self.current_level])
            ):
                if self.player.stealth:
                    self.player.Stealth()

                if self.player.self_class == "Rogue":
                    Lighting_Strike(self.player)
                else:
                    Circle_of_death(self.player)

            if (
                pg.mouse.get_pressed()[2]
                and not self.player.inmovement
                and not any(enem.inmovement for enem in self.enemy[self.current_level])
            ):
                # manage the player's movements
                self.click = "RIGHT"
                self.player.path = []
                mouse_position = pg.mouse.get_pos()
                end = Node(self, 0, 0)
                start = self.player.get_current_position(self.current_level)
                try:
                    mouse_node = self.grid[self.current_level][
                        int(
                            (mouse_position[1] - self.camera.get_pos()[1])
                            / settings.TILESIZE
                        )
                    ][
                        int(
                            (mouse_position[0] - self.camera.get_pos()[0])
                            / settings.TILESIZE
                        )
                    ]
                except IndexError:
                    break
                if event.type == pg.MOUSEBUTTONDOWN or mouse_node != end:
                    # if the right click is pressed or the end is not the same as initialy
                    flush_path(self)
                    start = self.player.get_current_position(self.current_level)
                    end = mouse_node
                    if (
                        end != 0
                        and (not end.is_barrier)
                        and (start is not end)
                        and (end in self.player.reachables[self.current_level])
                    ):
                        self.pm = astar(self, self.player, start, end)
                        draw_path(self)
                    if (
                        (end.is_barrier)
                        and (start is not end)
                        and (
                            math.sqrt(
                                ((end.x - start.x) ** 2) + ((end.y - start.y) ** 2)
                            )
                            < 2 * settings.TILESIZE
                        )
                    ):
                        for pnj in self.sprites[self.current_level]["J"]:
                            if end == pnj.node:
                                pnj.talk()
                                break
                        for pnj in self.sprites[self.current_level]["M"]:
                            if end == pnj.node:
                                pnj.talk()
                                break
                        for container in self.sprites[self.current_level]["C"]:
                            if end == container.node:
                                container.open(self)
                                break
            if (
                self.click == "RIGHT"
                and event.type == pg.MOUSEBUTTONUP
                and not self.player.inmovement
                and self.player.path
                and self.player.pm > settings.TILESIZE
            ):
                # when the right click is released and the player was not in movement before
                self.player.reachables[self.current_level] = []
                self.click = ""
                self.player.bmove = True
                self.player.reach_draw = False
                self.player.pm -= self.pm
                flush_path(self)
                flush_reachable(self)

            if self.player.is_casting:
                draw_aoe_area(self)


def spawn(self):
    """method that spawn new enemy if not enough"""
    if len(self.enemy[self.current_level]) < 5:
        random_position(self, 10)


def new(self):
    """initialize the game : it creates the grid of the map,
    creates the sprites and initialize the g and f_score for a_star"""
    self.grid[self.current_level] = []
    self.enemy[self.current_level] = []
    self.first = True
    self.mmap_group[self.m_current_level] = pg.sprite.Group()
    self.sprites[self.current_level] = {
        nouns: pg.sprite.Group()
        for nouns in {
            "A",
            "W",
            "MF",
            "G",
            "Pa",
            "R",
            "F",
            "E",
            "S",
            "D",
            "Po",
            "BP",
            "ZG",
            "DF",
            "AOE_ZONE",
            "AOE",
            "J",
            "M",
            "C",
            "V",
        }
    }
    if self.player:
        self.sprites[self.current_level]["A"].add(self.player)

    create_map(self, self.map.data)
    self.focus = self.player
    self.camera.update(self.focus)
    random_position(self, 10)
    for row in self.grid[self.current_level]:
        for node in row:
            if node != 0:
                node.neighbors.clear()
                if not node.is_barrier:
                    node.find_neighbors()
    self.player.reachables[self.current_level] = []

    self.update()


def random_position(self, num_enemy):
    """generate num_enemy enemy at random position"""
    available_position = [
        (y, x)
        for y in range(1, len(self.map.data))
        for x in range(1, len(self.map.data[y]))
        if self.map.data[y][x] == "."
    ]
    enemy_position = []
    for _ in range(num_enemy):
        while True:
            (y_pos, x_pos) = choice(available_position)
            if (y_pos, x_pos) not in enemy_position:
                enemy_position.append((y_pos, x_pos))
                self.enemy[self.current_level].append(Enemy(self, x_pos, y_pos))
                break


def console_menu(self):
    """the menu for console that has to be draw when the user press tab"""

    self.my_input = Input(
        self.screen.get_width() / 2 - 300 / 2,
        self.screen.get_height() / 2 - 50 / 2,
        (300, 50),
        name="Console",
        text="",
    )
    self.my_input.istyping = True


def console(player, input):
    """Manage all the command that the user type in the console


    List of all command :
        /set Str int
        /set Int int
        /set Con int
        /set Wis int
        /set Dex int
        /set Cha int
        /set Level int

        /give item int[1-43]

        /heal

        /kill

        /sucide

        Args:
    player (Player): The player that is currently used by the user
    input (String): the command that the user type in the console
    """
    player_input = input.split()
    command = player_input[0]
    node_list = []
    if len(player_input) >= 2:
        first_param = player_input[1]
    if len(player_input) >= 3:
        second_param = player_input[2]

    if command == "/set" and len(player_input) == 3:
        if first_param in player.dic_player:
            if second_param.isdigit():
                player.dic_player[first_param] = int(second_param)
                if first_param == "level":
                    player.dic_player["xp"] = 0
                    player.dic_player["carac point"] += int(second_param)

                player.game.log["log"].add_log(
                    "You set your : " + first_param + " at " + second_param
                )

            else:
                player.game.log["log"].add_log("Invalid parameter for set please retry")

    if command == "/heal":
        player.health = player.dic_player["Con"] * 10
        player.mana = player.dic_player["Int"] * 10
        player.game.log["log"].add_log("Invalid parameter for set please retry")

    if len(player_input) == 3 and command == "/give" and first_param == "item":
        if second_param.isdigit() and 1 <= int(second_param) <= 43:
            item = Item(int(second_param), player.game.all_item)
            player.inventory.add_item(int(second_param))
            player.game.log["log"].add_log(
                "You add to your inventory : " + str(item.name)
            )
        else:
            player.game.log["log"].add_log(
                "Invalid parameter for give item please retry"
            )

    if len(player_input) == 3 and command == "/give" and first_param == "gold":
        if second_param.isdigit():
            player.inventory.gold += int(second_param)
        else:
            player.game.log["log"].add_log(
                "Invalid parameter for give item please retry"
            )
    if command == "/kill":
        for row in player.game.grid[player.game.current_level]:
            for node in row:
                t = map(
                    sub,
                    node.get_pos(),
                    player.get_current_position(player.game.current_level).get_pos(),
                )

                test = tuple([abs(elt) for elt in t])
                if ((test[0]) <= settings.PM) and ((test[1]) <= settings.PM):
                    node_list.append(node)
        all_enemy = [
            enemy
            for enemy in player.game.enemy[player.game.current_level]
            if (enemy.get_current_position(player.game.current_level) in node_list)
        ]

        for enemy in all_enemy:
            enemy.health = 0

        player.game.log["log"].add_log("You kill every enemy around you")

    if command == "Hugod":
        for i in range(1338):
            player.game.log["log"].add_log(
                "I love python " + str(i) + " Welome to LEET"
            )

    if command == "/sucide":
        player.health = 0
    player.game.my_input.text = ""


def pause(self):
    """method that generate the pause menu when good key is pressed"""
    pg.draw.rect(
        self.screen,
        (10, 10, 10),
        ((settings.WIDTH - 150) // 2, (settings.HEIGHT - 300) // 2, 150, 300),
    )
    if not self.buttons:
        self.buttons["shortcut"] = Button(
            (settings.WIDTH - 150) // 2 + 10,
            (settings.HEIGHT - 300) // 2 + 35,
            (150 - 20, 30),
            "shortcut",
            (200, 200, 200),
        )
        self.buttons["save & quit"] = Button(
            (settings.WIDTH - 150) // 2 + 10,
            (settings.HEIGHT - 300) // 2 + 95,
            (150 - 20, 30),
            "save & quit",
            (200, 200, 200),
        )
        self.buttons["save"] = Button(
            (settings.WIDTH - 150) // 2 + 10,
            (settings.HEIGHT - 300) // 2 + 155,
            (150 - 20, 30),
            "save",
            (200, 200, 200),
        )


def shortcut(self):
    """method that generate the shortcut menu when good key is pressed
    the menu is modular"""
    for i, key in enumerate(self.bind):

        self.buttons[key] = Button(
            (((i + 1) * settings.SPACING) // settings.HEIGHT) * (settings.WIDTH // 3)
            + 50,
            ((i) % (settings.HEIGHT // settings.SPACING) * settings.SPACING) + 50,
            (150 - 20, 30),
            key,
            (200, 200, 200),
        )
        self.inputs[key] = Input(
            (((i + 1) * settings.SPACING) // settings.HEIGHT) * (settings.WIDTH // 3)
            + 50
            + self.buttons[key].rect.width
            + 50,
            ((i) % (settings.HEIGHT // settings.SPACING) * settings.SPACING) + 50,
            (130, 30),
            "",
            pg.key.name(self.bind[key]),
        )


def change_player(self, class_to_change):
    """method that change current_player"""
    pass_turn = False
    old = self.player.self_class
    self.players[self.player.self_class] = self.player
    self.players[class_to_change].pos = self.player.pos
    self.players[class_to_change].turn = self.player.turn
    self.players[class_to_change].pm = self.player.pm
    self.players[class_to_change].rot = self.player.rot
    self.player.path = []
    if not self.player.can_attack or not self.player.spell:
        pass_turn = True
    self.sprites[self.current_level]["A"].remove(self.player)
    self.player = self.players[class_to_change]
    self.sprites[self.current_level]["A"].add(self.player)
    self.player.reachables[self.current_level] = []
    self.player.reach_draw = True
    self.player.inmovement = False
    self.player.path = []
    if pass_turn:
        self.players[old].can_attack = True
        self.players[old].spell = True
        turn(self.player)
    self.player.update_name()
