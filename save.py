from draw import draw_reachable, flush_reachable, flush_path
import pickle
import pygame
from tiledmap import Map
import os
from player import Player
from sprites import (
    Ground,
    Wall,
    Fog_of_War,
    Portal,
    Back_Portal,
    Void,
)
from pnj import Pnj
from container import Container
from enemy import Enemy
import settings
import math
from inventory import Inventory

vec = pygame.math.Vector2


def load(self, save_name):
    path = os.path.dirname(__file__) + "/save"
    path = path + "/" + save_name + ".pickle"
    self.path_.clear()
    self.mmap_group.clear()
    self.sprites.clear()
    with open(path, "rb") as file:
        b = pickle.load(file)
        self.path_ = b["path"]
    for cpt in range(len(b["path"]) - 1):
        self.grid[cpt] = []
        self.mmap_group[cpt] = pygame.sprite.Group()
        self.player.reachables[cpt] = []
        self.current_level = cpt
        self.m_current_level = cpt

        self.sprites[cpt] = {
            nouns: pygame.sprite.Group()
            for nouns in {
                "A",
                "W",
                "G",
                "MF",
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
                "S",
                "AOE_ZONE",
                "AOE",
                "J",
                "M",
                "C",
                "V",
            }
        }
        tmp = self.path_[cpt].split("\\")
        tmp = tmp[len(tmp) - 2] + "\\" + tmp[len(tmp) - 1]
        tmp = os.path.dirname(__file__) + "\\" + tmp
        map_tmp = Map(tmp)
        create_map(self, map_tmp.data, True)
    flush_path(self)
    flush_reachable(self)
    var_dic = self.player.__dict__
    for key in b["player"]:
        var_dic[key] = b["player"][key]
    for lvl in b["fog"]:
        self.sprites[lvl]["A"].add(self.player)
        self.current_level = lvl
        self.m_current_level = lvl
        for sprit in self.sprites[lvl]["F"]:
            self.sprites[lvl]["F"].remove(sprit)
            self.sprites[lvl]["A"].remove(sprit)
        for tupl in b["fog"][lvl]:
            self.sprites[lvl]["F"].add(Fog_of_War(self, *tupl))
    self.attributed_to_enemy = []
    for lvl in b["enemy"]:
        self.enemy[lvl] = []
        self.current_level = lvl
        for sprit in self.sprites[lvl]["E"]:
            self.sprites[lvl]["E"].remove(sprit)
            self.sprites[lvl]["A"].remove(sprit)
        for pos in b["enemy"][lvl]:
            self.enemy[lvl].append(Enemy(self, *pos))
    self.current_level = b["current_level"]
    self.log["log"].log_list = b["log"]
    self.player.reach_draw = True
    self.player.turn_text = pygame.font.SysFont("Cascadia code", 60).render(
        str(self.player.turn), True, settings.WHITE
    )
    self.player.outline = pygame.font.SysFont("Cascadia code", 60).render(
        str(self.player.turn), True, settings.BLACK
    )
    self.player.dic_player = b["player"]["dic_player"]
    self.player.player_sheet.portrayal = b["player"]["portrayal"]
    self.player.player_sprite = b["player"]["player_sprite"]
    self.player.player_sheet.dic_player = self.player.dic_player
    self.player.player_sheet.initialised = True
    self.player.stealth = b["player"]["stealth"]
    self.player.dic_inventory = b["inventory"]

    self.player.inventory = Inventory(
        self, self.player.dic_player, self.player.dic_inventory
    )
    self.bind = b["bind"]
    for key in self.players:
        var_dic = self.players[key].__dict__
        for _ in b["players"][key]:
            var_dic[_] = b["players"][key][_]
        self.players[key].reach_draw = True
        self.players[key].turn_text = pygame.font.SysFont("Cascadia code", 60).render(
            str(self.players[key].turn), True, settings.WHITE
        )
        self.players[key].outline = pygame.font.SysFont("Cascadia code", 60).render(
            str(self.players[key].turn), True, settings.BLACK
        )
        self.players[key].dic_player = b["players"][key]["dic_player"]
        self.players[key].player_sheet.portrayal = b["players"][key]["portrayal"]
        self.players[key].player_sprite = b["players"][key]["player_sprite"]
        self.players[key].player_sheet.dic_player = self.players[key].dic_player
        self.players[key].player_sheet.initialised = True
        self.players[key].stealth = b["players"][key]["stealth"]
        self.players[key].dic_inventory = b["players"][key]["inventory"]
        self.players[key].inventory = Inventory(
            self, self.players[key].dic_player, self.players[key].dic_inventory
        )
        self.players[key].asmove = False
    self.focus = self.player
    self.first = True
    tmp = self.path_[self.current_level].split("\\")
    tmp = tmp[len(tmp) - 2] + "\\" + tmp[len(tmp) - 1]
    tmp = os.path.dirname(__file__) + "\\" + tmp
    self.map = Map(tmp)
    for row in self.grid[self.current_level]:
        for node in row:
            if node != 0:
                node.neighbors.clear()
                if not node.is_barrier:
                    node.find_neighbors()
    flush_reachable(self)
    draw_reachable(self)
    self.player.update_name()
    self.player.spell_surface = self.player.draw_player_skill()


def save(self, save_name):
    path = os.path.dirname(__file__) + "/save"
    if not os.path.exists(path):
        os.mkdir(path)
    path = path + "/" + save_name + ".pickle"

    with open(path, "wb") as write_file:
        dic = {}
        dic["bind"] = self.bind
        dic["current_level"] = self.current_level
        dic["path"] = self.path_
        dic["player"] = self.player.getstate()
        dic["player"]["portrayal"] = self.player.player_sheet.portrayal
        dic["player"]["stealth"] = self.player.stealth
        dic["fog"] = {}
        dic["log"] = self.log["log"].log_list
        z_data = {}
        dic["enemy"] = {}
        dic["players"] = {}
        dic["inventory"] = {
            "volume": self.player.inventory.volume,
            "weight": self.player.inventory.weight,
            "stuff_equipped": self.player.inventory.stuff_equipped,
            "gold": self.player.inventory.gold,
        }
        _ = []
        for item in self.player.inventory.liste:
            if item:
                _.append([item.item_id, item.stack])
            else:
                _.append(None)
        dic["inventory"]["liste"] = _
        for class_ in self.players:
            dic["players"][class_] = self.players[class_].getstate()
            dic["players"][class_]["inventory"] = {
                "volume": self.players[class_].inventory.volume,
                "weight": self.players[class_].inventory.weight,
                "stuff_equipped": self.players[class_].inventory.stuff_equipped,
                "gold": self.players[class_].inventory.gold,
            }
            _ = []
            for item in self.players[class_].inventory.liste:
                if item:
                    _.append([item.item_id, item.stack])
                else:
                    _.append(None)
            dic["players"][class_]["inventory"]["liste"] = _
            dic["players"][class_]["portrayal"] = self.players[
                class_
            ].player_sheet.portrayal
            dic["players"][class_]["stealth"] = self.players[class_].stealth
        for cpt in range(len(self.path_) - 1):
            data = [
                (sprites.x, sprites.y, sprites.tipe, sprites.alpha)
                for sprites in self.sprites[cpt]["F"]
            ]
            z_data[cpt] = [
                (
                    enemy.get_current_position(cpt).col,
                    enemy.get_current_position(cpt).row,
                    self.player.turn,
                    enemy.rarity,
                )
                for enemy in self.enemy[cpt]
            ]
            dic["fog"][cpt] = data
            dic["enemy"][cpt] = z_data[cpt]
        pickle.dump(dic, write_file, pickle.HIGHEST_PROTOCOL)


def create_map(self, map_data, _load=False):
    self.enemy[self.current_level] = []
    for row, tiles in enumerate(map_data):
        self.grid[self.current_level].append([])
        for col, tile in enumerate(tiles):
            if tile == "X":
                tmp = self.path_[self.current_level].split("\\")
                tmp = tmp[len(tmp) - 2] + "\\" + tmp[len(tmp) - 1]
                tmp = os.path.dirname(__file__) + "\\" + tmp
                read_ = open(tmp, "r+")
                read_.seek(self.map.offset, 0)
                tmp = read_.read()
                map_read = tmp.split(" ")
                read_.close()
                if not _load:
                    self.path_[self.current_level + 1] = os.path.join(
                        self.map_folder, map_read[0]
                    )
                portal_sprite = Portal(self, col, row, self.path_[self.current_level])
                self.portal_pos[self.current_level] = [col, row]
                self.sprites[self.current_level]["G"].add(portal_sprite)
                self.sprites[self.current_level]["Po"].add(portal_sprite)
                if not _load:
                    self.sprites[self.current_level]["F"].add(
                        Fog_of_War(self, col, row, "ground")
                    )
                self.grid[self.current_level][row].append(portal_sprite.node)
            if tile == "1":
                wall = Wall(self, col, row)
                self.sprites[self.current_level]["W"].add(wall)
                if not _load:
                    self.sprites[self.current_level]["F"].add(
                        Fog_of_War(self, col, row, "wall")
                    )
                self.grid[self.current_level][row].append(wall.node)
            elif tile == "P":
                self.pcol[self.current_level] = col
                self.prow[self.current_level] = row
                if self.current_level > 0:
                    if not _load:
                        self.sprites[self.current_level]["F"].add(
                            Fog_of_War(self, col, row, "ground")
                        )
                    back_portal = Back_Portal(self, col, row)
                    self.sprites[self.current_level]["G"].add(back_portal)
                    self.sprites[self.current_level]["BP"].add(back_portal)
                    self.grid[self.current_level][row].append(back_portal.node)
                else:
                    ground = Ground(self, col, row)
                    self.sprites[self.current_level]["G"].add(ground)
                    if not _load:
                        self.sprites[self.current_level]["F"].add(
                            Fog_of_War(self, col, row, "ground", 255)
                        )
                    self.grid[self.current_level][row].append(ground.node)
            elif tile == ".":
                ground = Ground(self, col, row)
                self.sprites[self.current_level]["G"].add(ground)
                if not _load:
                    self.sprites[self.current_level]["F"].add(
                        Fog_of_War(self, col, row, "ground", 255)
                    )
                self.grid[self.current_level][row].append(ground.node)
            elif tile == "J":
                perso = Pnj(self, col, row, False)
                self.sprites[self.current_level]["J"].add(perso)
                if not _load:
                    self.sprites[self.current_level]["F"].add(
                        Fog_of_War(self, col, row, "wall", 255)
                    )
                self.grid[self.current_level][row].append(perso.node)
            elif tile == "M":
                perso = Pnj(self, col, row, True)
                self.sprites[self.current_level]["M"].add(perso)
                if not _load:
                    self.sprites[self.current_level]["F"].add(
                        Fog_of_War(self, col, row, "wall", 255)
                    )
                self.grid[self.current_level][row].append(perso.node)
            if tile == "C":
                container = Container(self, col, row)
                self.sprites[self.current_level]["C"].add(container)
                if not _load:
                    self.sprites[self.current_level]["F"].add(
                        Fog_of_War(self, col, row, "wall")
                    )
                self.grid[self.current_level][row].append(container.node)
            elif tile == "0":
                void = Void(self, col, row)
                void.node.make_barrier()
                self.grid[self.current_level][row].append(void.node)
                if not _load:
                    self.sprites[self.current_level]["V"].add(void)
            elif tile == "B":
                ground = Ground(self, col, row)
                self.sprites[self.current_level]["G"].add(ground)
                self.grid[self.current_level][row].append(ground.node)
                boss = Enemy(self, col, row, 0, (4, (255, 215, 0)))
                if not _load:
                    self.enemy[self.current_level].append(boss)
                    self.sprites[self.current_level]["F"].add(
                        Fog_of_War(self, col, row, "ground")
                    )

        if all(isinstance(node, Void) for node in self.grid[self.current_level][row]):
            self.grid[self.current_level].pop()
            break
    if self.player:
        self.player.pos = (
            vec(
                self.pcol[self.current_level] + 0.5, self.prow[self.current_level] + 0.5
            )
            * settings.TILESIZE
        )
    else:
        for key in self.players:
            if self.chara_dic:
                self.players[key] = Player(
                    self,
                    self.pcol[self.current_level],
                    self.prow[self.current_level],
                    chara_dic=self.chara_dic[key],
                )
            else:
                self.players[key] = Player(
                    self, self.pcol[self.current_level], self.prow[self.current_level]
                )
            self.sprites[self.current_level]["A"].remove(self.players[key])
        if self.chara_dic:
            self.player = Player(
                self,
                self.pcol[self.current_level],
                self.prow[self.current_level],
                chara_dic=self.chara_dic["Barbarian"],
            )
        else:
            self.player = Player(
                self, self.pcol[self.current_level], self.prow[self.current_level]
            )
    for row in self.grid[self.current_level]:
        for node in row:
            if node != 0:
                node.neighbors.clear()
                if not node.is_barrier:
                    node.find_neighbors()
    self.g_score[self.current_level] = {
        spot: float(math.inf)
        for row in self.grid[self.current_level]
        if row != 0
        for spot in row
    }
    self.f_score[self.current_level] = {
        spot: float(math.inf)
        for row in self.grid[self.current_level]
        if row != 0
        for spot in row
    }
