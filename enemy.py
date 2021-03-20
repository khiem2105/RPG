"""ennemy module that contains Enemy class"""
from os import path
import random
import pygame as pg
from draw import update_draw
from entity import Entity
from box import Button
from inventory import Item
from pathfinding import Node, astar
from sprites import Zombie_ground
import settings

vec = pg.math.Vector2


class Enemy(Entity):
    """Class Enemy that controls the mob that attacks the player"""

    def __init__(self, game, x, y, turn=-1, rarity=None):
        super().__init__(game, x, y)

        self.health = settings.MOB_HEALTH
        self.isseen = False
        if turn == -1:
            self.turn = max(self.game.player.turn - 1, 0)
        else:
            self.turn = turn
        self.current = self.game.current_level
        self.player_node = Node(self, 20, 20)
        self.random_node = None
        self.ground_tile = None
        self.enemy_collection = ["WOLF", "MINOTAUR", "GOBLIN", "SKELETON", "ZOMBIE"]
        # allow to have only one type of enemy per level
        self.type_enemy = self.enemy_collection[game.current_level % 5]
        # allow to obtain the enemy's name in the dictionary
        # (according to the current level) and access to the name which indicate
        #  the path to go to the image associated with the enemy's type
        self.name_image_enemy = self.type_enemy[:2]
        # addition to a "E" group for enemies
        self.looting = None
        self.item = []
        if game.editor:
            self.pos = vec((x + 0.5) * settings.TILESIZE, (y + 0.5) * settings.TILESIZE)
            self.image = pg.transform.rotate(self.game.img["MI"], self.rot)
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
        if not game.editor:
            for quest in self.game.quest.quest_list:
                if "enemy" in self.game.quest.quest_list[str(quest)]:
                    if (
                        self.game.quest.quest_list["7"]["enemy"]
                        == self.type_enemy
                        and len(self.game.sprites[self.current]["E"]) < 6
                        and len(self.game.attributed_to_enemy) < 12
                    ):
                        self.quest_item = []
                        while len(self.quest_item) < 2:
                            rand = random.randint(31, 43)
                            item = Item(rand, self.game.all_item)
                            if rand not in self.game.attributed_to_enemy:
                                self.quest_item.append(item)
                                self.game.attributed_to_enemy.append(rand)
                    elif (
                        self.game.quest.quest_list["4"]["enemy"]
                        == self.type_enemy
                        and len(self.game.sprites[self.current]["E"]) == 6
                    ):
                        self.quest_item = [Item(43, self.game.all_item)]
                    else:
                        self.quest_item = None
            self.game.sprites[self.current]["E"].add(self)
            self.quest = {}
            self.looted = False
            self.looting_pos = None
            self.level = self.current + 1
            for key in self.game.quest.quest_list:
                if self.game.quest.quest_list[key]["type"] != "0":
                    if self.game.quest.quest_list[key]["enemy"] == self.type_enemy:
                        self.quest[key] = self.game.quest.quest_list[key]

            if not rarity:
                self.rarity = self.rand_rarity()
            else:
                self.rarity = rarity
            self.name = pg.font.SysFont("Cascadia code", 20).render(
                self.type_enemy + " - " + str(self.level), True, self.rarity[1]
            )  # permet d'afficher au dessus des ennemis leur nom/type
            self.outline = pg.font.SysFont("Cascadia code", 20).render(
                self.type_enemy + " - " + str(self.level), True, settings.BLACK
            )
            self.get_current_position(self.current).make_barrier()
            self.dex = 10
            self.item = self.generate_item()
            if not self.item:
                self.item = []
            self.item.append(self.loot_gold())
            if self.quest_item:
                self.item.extend(self.quest_item)
            if self.rarity[0] == 4:
                self.damage = 23 * self.level
                self.health = 500 * self.level

            else:
                self.damage = (
                    settings.ZOMBIE_DAMAGE
                    * ((self.rarity[0] + 1) // 2)
                    * (self.level + 1)
                    // 2
                )
            self.max_health = self.health

    def update(self):
        """method that manages the enemy updtae (pos,vel,rot,attack...)"""
        if not self.game.editor:
            self.image = pg.transform.rotate(
                self.game.img[self.name_image_enemy], self.rot
            )
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            if self.health < 0:
                self.health = 0
            if self.looting and self.game.player.inmovement:
                self.looting = None
                self.game.buttons.clear()
            if len(self.item) <= 0:
                self.looted = True
            if self.current != self.game.current_level:
                return
            if self.health > 0:
                distance = (self.game.player.pos - self.pos).length()
                if (
                    distance <= settings.ATTACK_RADIUS
                    and not self.inmovement
                    and not self.path
                ):
                    if not self.isseen:
                        self.isseen = True
                elif self.isseen and not self.inmovement and not self.path:
                    self.isseen = False
                    if self.ground_tile:
                        self.game.sprites[self.game.current_level]["ZG"].remove(
                            self.ground_tile
                        )
                if self.turn < self.game.player.turn:
                    if (
                        self.isseen
                        and (
                            not self.game.player.path
                            and not self.game.player.inmovement
                            and not self.game.player.stealth
                        )
                        and not any(
                            enem.inmovement
                            for enem in self.game.enemy[self.game.current_level]
                            if enem != self and enem.isseen
                        )
                    ):
                        self.movement()
                    elif (
                        not self.isseen
                        or self.game.player.stealth
                        and self.rarity[0] < 4
                    ):
                        self.patrol()
                    elif self.rarity[0] == 4:
                        self.asmove = True
                    if distance < settings.TILESIZE * 2 and not self.asmove:
                        self.asmove = True
                    if not self.path and not self.inmovement and self.isseen:
                        self.rot = (self.game.player.pos - self.pos).angle_to(vec(1, 0))
                        self.image = pg.transform.rotate(
                            self.game.img[self.name_image_enemy], self.rot
                        )
                        self.rect = self.image.get_rect()
                        self.rect.center = self.pos
                    if (
                        distance < 2 * settings.TILESIZE
                        and not self.inmovement
                        and not self.path
                        and self.isseen
                    ):
                        self.attack()
                    if (
                        not self.path
                        and not self.inmovement
                        and self.asmove
                        and self.turn < self.game.player.turn
                    ):
                        self.next_turn()
            elif self.turn < self.game.player.turn:
                self.turn = self.game.player.turn

            if self.health <= 0 and self.looted:
                if self.get_current_position(self.current).is_barrier:
                    self.get_current_position(self.current).unmake_barrier()
                if self.ground_tile:
                    self.game.sprites[self.game.current_level]["ZG"].remove(
                        self.ground_tile
                    )
                    self.game.mmap_group[self.game.current_level].remove(
                        self.ground_tile.map
                    )
                self.game.sprites[self.game.current_level]["E"].remove(self)
                self.game.enemy[self.game.current_level].remove(self)
                self.give_xp()
                self.loot_gold()
                self.kill()
                self.game.player.qcheck = True
                for quest in self.quest:
                    if (
                        quest in self.game.player.quest
                        and self.game.quest.quest_list[quest]["type"] == "1"
                    ):
                        self.game.player.quest[quest] = min(
                            self.game.player.quest[quest] + 1,
                            int(self.game.quest.quest_list[quest]["objective"]),
                        )

                    elif (
                        quest in self.game.player.quest
                        and self.game.quest.quest_list[quest]["type"] == "2"
                        and Item(43, self.game.all_item)
                        in self.game.player.inventory.liste
                    ):
                        self.game.player.quest[quest] = int(
                            self.game.quest.quest_list[quest]["objective"]
                        )

                    elif (
                        quest in self.game.player.quest
                        and self.game.quest.quest_list[quest]["type"] == "3"
                    ):
                        for i in range(31, 43):
                            if (
                                Item(i, self.game.all_item)
                                in self.game.player.inventory.liste
                            ):
                                self.game.player.quest[quest] += 1

                for row in self.game.grid[self.game.current_level]:
                    for node in row:
                        if node != 0:
                            node.neighbors.clear()
                            if not node.is_barrier:
                                node.find_neighbors()
                self.game.player.reach_draw = True

            if self.isseen:
                for enemy in self.game.sprites[self.game.current_level]["E"]:
                    if (
                        enemy.pos - self.pos
                    ).length() <= settings.SHARE_KNOWLEDGE_RADIUS:
                        enemy.isseen = True
                if not self.ground_tile:
                    self.ground_tile = Zombie_ground(
                        self.game,
                        self.get_current_position(self.current).col,
                        self.get_current_position(self.current).row,
                    )
                    self.game.sprites[self.game.current_level]["ZG"].add(
                        self.ground_tile
                    )

    def generate_item(self):
        """method that generate items that the mob will drop"""
        rand = random.randint(1, 20)
        dic = {
            "MINOTAUR": 100,
            "SKELETON": 101,
            "GOBLIN": 102,
            "WOLF": 103,
            "ZOMBIE": 104,
        }
        cpt = 0
        item = None
        while rand + self.rarity[0] * 2 > 19:
            if not cpt:
                item = Item(dic[self.type_enemy], self.game.all_item)
            cpt += 1
            rand = random.randint(1, 20)
        if item:
            item.stack = cpt
            return [item]

    def attack(self):
        """method that manages all the things related to the
        damage inflicted to the player"""
        target_position = self.get_current_position(self.game.current_level).get_pos()
        self.game.player.rot = (target_position - self.game.player.pos).angle_to(
            vec(1, 0)
        )
        self.game.player.image = pg.transform.rotate(
            self.game.img[self.game.player.player_sprite], self.game.player.rot
        )
        if self.game.player.avoid_attack():
            self.game.player.health -= (
                self.damage - self.game.player.dic_player["armor"]
            )
            self.game.log["log"].add_log(
                self.type_enemy
                + " : deals "
                + str(self.damage - self.game.player.dic_player["armor"])
                + " damage to player"
            )

    def take_dmg(self, damage):
        """The enemy does a roll 20 in order to know if he avoid attack
        if he does : he takes half dmg
        if not : take full dmg
        Args:
            damage (int): damage that should be taken
        """
        rng = random.randint(1, 20)
        if rng <= self.dex:
            self.health = max(self.health - damage / 2, 0)
            self.game.log["log"].add_log(
                self.type_enemy + " avoid attack, he tooks half dmg"
            )
        self.health = max(self.health - damage, 0)

    def draw_health(self, screen):
        """method that manage the drawing of mob's health
        need to be call at each frame"""
        if self.isseen:
            if self.rarity[0] < 4:
                if self.health / self.max_health > 0.6:
                    col = settings.GREEN
                elif self.health / self.max_health > 0.3:
                    col = settings.YELLOW
                else:
                    col = settings.RED

                width = int(self.rect.width * self.health / self.max_health)
                health_bar = pg.Rect(0, 0, width, 7)
                if self.health < self.max_health:
                    pg.draw.rect(self.image, col, health_bar)
            else:
                if self.health / self.max_health > 0.6:
                    col = settings.GREEN
                elif self.health / self.max_health > 0.3:
                    col = settings.YELLOW
                else:
                    col = settings.RED
                width = screen.get_width() * 0.5 * self.health / self.max_health
                name = pg.font.SysFont("Cascadia code", 32).render(
                    self.type_enemy + " - " + str(self.level), True, self.rarity[1]
                )
                health_bar = pg.Rect(screen.get_width() * 0.25, 20, width, 7)
                if self.health < self.max_health:
                    pg.draw.rect(screen, col, health_bar)
                    screen.blit(
                        name,
                        (
                            screen.get_width() // 2 - name.get_width() // 2,
                            20 - name.get_height(),
                        ),
                    )

    def movement(self):
        """method that manage the enemy's movement"""
        end = self.game.player.get_current_position(self.current)
        if end != self.player_node:
            self.path = []
            self.game.focus = self
            update_draw(self.game)
            self.player_node = end
            start = self.get_current_position(self.current)
            start.unmake_barrier()
            self.game.sprites[self.game.current_level]["ZG"].remove(self.ground_tile)
            for row in self.game.grid[self.game.current_level]:
                for node in row:
                    if node != 0:
                        node.neighbors.clear()
                        if not node.is_barrier:
                            node.find_neighbors()
            if not astar(self.game, self, start, self.player_node):
                self.turn += 1
                self.random_node = None
                self.asmove = False
                return
            if self.path:
                self.path.pop()
            self.bmove = True
        self.image = pg.transform.rotate(self.game.img[self.name_image_enemy], self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.move()
        pos_ = self.pos + self.vel * self.game.tick
        self.pos = vec(round(pos_[0]), round(pos_[1]))
        if not self.inmovement and not self.target and not self.path:
            self.next_turn()

    def loot(self):
        """method that manage when the player loot an enemy"""
        self.looting = pg.Surface((175, 350), pg.SRCALPHA, 32)
        if not self.looting_pos:
            self.looting_pos = pg.mouse.get_pos()
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, "img")
        self.looting.blit(pg.image.load(path.join(img_folder, "loot.png")), (0, 0))
        self.game.buttons.clear()
        if self.item:
            for cpt, item in enumerate(self.item):
                self.looting.blit(
                    pg.transform.scale(
                        pg.image.load(path.join(img_folder, item.img)),
                        (settings.TILESIZE, settings.TILESIZE),
                    ),
                    (15, 30 + 30 * 2 * cpt),
                )
                self.looting.blit(
                    pg.font.SysFont("cascadia code", 16).render(
                        item.name, True, settings.COMMON
                    ),
                    (75, 30 + settings.TILESIZE // 3 + 30 * 2 * cpt),
                )
                self.game.buttons[cpt] = Button(
                    self.looting_pos[0] + 12,
                    self.looting_pos[1] + 30 + 30 * 2 * cpt,
                    (150, settings.TILESIZE),
                    ennemy=(self, item),
                )
                if item.stack >= 2:
                    _ = pg.font.SysFont("Cascadia code", 32).render(
                        str(item.stack), True, settings.COMMON
                    )
                    self.looting.blit(
                        _,
                        (
                            15 - _.get_rect().width + settings.TILESIZE,
                            30 + 30 * 2 * cpt - _.get_rect().height,
                        ),
                    )

        else:
            self.game.buttons.clear()
            self.looted = True
            self.looting = None

    def patrol(self):
        """method that manage the enemy patrol when it's not seens"""
        while self.random_node is None or self.random_node.is_barrier:
            try:
                random_row = random.randrange(
                    max(1, self.get_current_position(self.current).row - 5),
                    min(
                        self.get_current_position(self.current).row + 5,
                        len(self.game.map.data),
                    ),
                )
                random_col = random.randrange(
                    max(
                        1,
                        self.game.grid[self.game.current_level][random_row][
                            self.get_current_position(self.current).col
                        ].col
                        - 6,
                    ),
                    min(
                        self.game.grid[self.game.current_level][random_row][
                            self.get_current_position(self.current).col
                        ].col
                        + 5,
                        len(self.game.map.data[random_row]),
                    ),
                )
                self.random_node = self.game.grid[self.game.current_level][random_row][
                    random_col
                ]
            except IndexError:
                pass
        start = self.get_current_position(self.current)
        start.unmake_barrier()
        for row in self.game.grid[self.game.current_level]:
            for node in row:
                if node != 0:
                    node.neighbors.clear()
                    if not node.is_barrier:
                        node.find_neighbors()
        pos_ = [
            (self.random_node.col + 0.5) * settings.TILESIZE,
            (self.random_node.row + 0.5) * settings.TILESIZE,
        ]
        self.pos = vec(round(pos_[0]), round(pos_[1]))
        self.asmove = True

    def next_turn(self):
        """method that manage the turn from the enemy"""
        self.turn = self.game.player.turn
        self.random_node = None
        self.asmove = False
        if self.isseen:
            if self.ground_tile:
                self.game.sprites[self.game.current_level]["ZG"].remove(
                    self.ground_tile
                )
                self.game.mmap_group[self.game.current_level].remove(
                    self.ground_tile.map
                )
            self.ground_tile = Zombie_ground(
                self.game,
                self.get_current_position(self.current).col,
                self.get_current_position(self.current).row,
            )
            self.game.sprites[self.game.current_level]["ZG"].add(self.ground_tile)
        if not self.get_current_position(self.current).is_barrier:
            self.get_current_position(self.current).make_barrier()
            for row in self.game.grid[self.game.current_level]:
                for node in row:
                    if node != 0:
                        node.neighbors.clear()
                        if not node.is_barrier:
                            node.find_neighbors()

    def rand_rarity(self):
        """rand rarity, use at initialisation """
        rand = random.randint(1, 100)
        if rand >= 95:
            return (3, settings.EPIC)
        if rand >= 80:
            return (2, settings.RARE)
        return (1, settings.COMMON)

    def give_xp(self):
        """method that give xp to player when enemy die"""
        if self.rarity[0] == 1:
            self.game.player.dic_player["xp"] += 20 * self.level
        if self.rarity[0] == 2:
            self.game.player.dic_player["xp"] += 40 * self.level
        if self.rarity[0] == 3:
            self.game.player.dic_player["xp"] += 80 * self.level
        if self.rarity[0] == 4:
            self.game.player.dic_player["xp"] += 160 * self.level

    def loot_gold(self):
        """method that rand how many gold the enemy will loot"""
        if self.rarity[0] == 1:
            rand_gold = random.randint(1, 4)
        elif self.rarity[0] == 2:
            rand_gold = random.randint(1, 6)
        elif self.rarity[0] == 3:
            rand_gold = random.randint(1, 8)
        elif self.rarity[0] == 4:
            rand_gold = 5
        else:
            rand_gold = 1
        tmp = Item(1000, self.game.all_item)
        tmp.stack = rand_gold
        return tmp
