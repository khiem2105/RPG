"""module that contains Inventory class"""
from os import path
import pygame as pg
import settings
from item import Item


class Inventory:
    """class that manage items that the player has in his inventory"""

    def __init__(self, game, dic_char=None, dic_inv=None, volume=100, pnj=False):
        self.char = dic_char
        self.all_item = game.all_item
        self.game = game
        self.pnj = pnj
        self.all_item = game.all_item
        self.screen = None
        # variables useful for display
        self.boxsize = 96
        # coordinates of the first case
        if self.pnj:
            self.xbegin = 126
            self.ybegin = 112
            self.coo_gold = (757, 137)
        else:
            self.xbegin = 597
            self.ybegin = 150
            self.coo_gold = (730, 65)
        # number of boxes for a line
        self.nbox = 4
        self.gap = 18
        self.imgsize = self.boxsize - self.gap
        self.coo_plastron = (407, 597)
        self.coo_helmet = (407, 412)
        self.coo_weapon = (407, 228)

        self.infoit = None
        self.gapitinfo = -150
        self.xlimit = 860
        self.ylimit = 590
        self.mouseinslot = {"slot": False, "equippedSlot": False}
        self.item_pos = None
        self.color = (171, 125, 0)

        if dic_inv is None:
            self.volume = volume  # volume = capacity of the l'inventaire
            self.weight = 0  # weight = how the inventory is filled
            # list of the ids of the items in the inventory
            self.liste = [None for _ in range(6 * self.nbox)]

            # juste pour tester
            for i in range(5):
                self.add_item(Item(i, self.all_item).item_id)

            self.gold = 0
            self.stuff_equipped = {"weapon": None, "plastron": None, "helmet": None}
        else:
            self.volume = self.get_volume(dic_char["Str"])
            self.liste = []
            for item in dic_inv["liste"]:
                if item:
                    self.liste.append(Item(item[0], self.all_item, item[1]))
                else:
                    self.liste.append(None)
            self.gold = dic_inv["gold"]
            self.stuff_equipped = dic_inv["stuff_equipped"]
            self.weight = self.gold / 10
            for item in self.liste:
                if item:
                    self.weight += item.weight
            for key in self.stuff_equipped:
                if self.stuff_equipped[key] is None:
                    continue
                item = Item(self.stuff_equipped[key], self.all_item)
                self.weight += item.weight

        self.isopen = False

        self.selected_item = None

        self.size = 24  # max number of slots

        self.game_folder = path.dirname(__file__)
        self.img_folder = path.join(self.game_folder, "img")

        if self.pnj:
            self.img = pg.image.load(
                path.join(self.img_folder, settings.INVENTORY_IMG_PNJ)
            ).convert_alpha()
        else:
            self.img = pg.image.load(
                path.join(self.img_folder, settings.INVENTORY_IMG)
            ).convert_alpha()

        self.img = pg.transform.scale(self.img, (1024, 768))
        self.selected = pg.image.load(
            path.join(self.img_folder, settings.INVENTORY_SELECTED)
        ).convert_alpha()
        self.selected = pg.transform.scale(self.selected, (self.imgsize, self.imgsize))
        self.fontbackground = pg.image.load(
            path.join(self.img_folder, "backgroundFont.png")
        ).convert_alpha()

        # for drag and drop
        self.itimg = None
        self.clic = False
        self.helditem = None
        self.drop = False
        self.helditemslot = None
        self.mouse_position = None
        self.mouse_offset = (
            (self.boxsize - self.gap) / -2,
            (self.boxsize - self.gap) / -2,
        )

    # add an item in the inventory

    def add_item(self, item_id, stack=1):
        """we check the inventory is not full first"""
        try:
            self.game.player.qcheck = True
        except AttributeError:
            pass
        self.weight += self.all_item[item_id]["weight"] * stack
        for item in self.liste:
            if item and item.item_id == item_id and item.stack < item.max_stack:
                item.stack += stack
                return True
        for i, _ in enumerate(self.liste):
            if self.liste[i] is None:
                self.liste[i] = Item(item_id, self.all_item, stack)
                return True
        return False

    # remove an item from the inventory

    def remove_item(self, item_id):
        """it is the position of the item in liste"""
        for i, _ in enumerate(self.liste):
            if self.liste[i] and self.liste[i].item_id == item_id:
                if item_id not in self.stuff_equipped:
                    itweigth = self.all_item[item_id]["weight"]
                    self.weight -= itweigth
                self.liste[i] = None
                self.game.player.qcheck = True
                return

    # clear the inventory

    def clear(self):
        """clear inventory"""
        self.weight = 0
        self.liste = []

    def open(self):
        """open the inventory and draw"""
        self.isopen = True
        screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
        while self.isopen:
            self.draw(screen)

            self.event()

    def draw(self, screen):
        """draw the inventory"""
        screen.fill(self.color)
        text_size = 20
        # bg_col = [0,0,0]
        text_col = [255, 255, 255]
        font = pg.font.SysFont("georgia", text_size)

        # display the inventory background
        screen.blit((self.img), (0, 0))

        # display of all items which are in the inventory
        for i in range(len(self.liste)):
            if (i == self.helditemslot) or (self.liste[i] is None):
                continue

            item = self.liste[i]
            itimg = pg.image.load(path.join(self.img_folder, item.img)).convert_alpha()
            itimg = pg.transform.scale(itimg, (self.imgsize, self.imgsize))
            screen.blit(
                (itimg),
                (
                    self.xbegin + i % self.nbox * self.boxsize,
                    i // self.nbox * self.boxsize + self.ybegin,
                ),
            )
            if self.selected and i == self.selected_item:
                screen.blit(
                    (self.selected),
                    (
                        self.xbegin + i % self.nbox * self.boxsize,
                        i // self.nbox * self.boxsize + self.ybegin,
                    ),
                )
            if item.stack >= 2:
                _ = pg.font.SysFont("Cascadia code", 32).render(
                    str(item.stack), True, settings.COMMON
                )
                screen.blit(
                    _,
                    (
                        self.xbegin
                        + i % self.nbox * self.boxsize
                        - _.get_rect().width
                        + self.boxsize
                        - 10,
                        i // self.nbox * self.boxsize
                        + self.ybegin
                        - _.get_rect().height
                        + self.boxsize
                        - 10,
                    ),
                )

        if self.stuff_equipped["weapon"] is not None and self.helditemslot != "weapon":
            itimg = pg.image.load(
                path.join(
                    self.img_folder,
                    self.all_item[(self.stuff_equipped["weapon"])]["img"],
                )
            ).convert_alpha()
            itimg = pg.transform.scale(itimg, (self.imgsize, self.imgsize))
            screen.blit(itimg, (self.coo_weapon))
            if self.mouseinslot["equippedSlot"] == "weapon" == self.selected_item:
                screen.blit((self.selected), (self.coo_weapon))

        if (
            self.stuff_equipped["plastron"] is not None
            and self.helditemslot != "plastron"
        ):
            itimg = pg.image.load(
                path.join(
                    self.img_folder,
                    self.all_item[(self.stuff_equipped["plastron"])]["img"],
                )
            ).convert_alpha()
            itimg = pg.transform.scale(itimg, (self.imgsize, self.imgsize))
            screen.blit(itimg, (self.coo_plastron))
            if self.mouseinslot["equippedSlot"] == "plastron" == self.selected_item:
                screen.blit((self.selected), (self.coo_plastron))

        if self.stuff_equipped["helmet"] is not None and self.helditemslot != "helmet":
            itimg = pg.image.load(
                path.join(
                    self.img_folder,
                    self.all_item[(self.stuff_equipped["helmet"])]["img"],
                )
            ).convert_alpha()
            itimg = pg.transform.scale(itimg, (self.imgsize, self.imgsize))
            if self.mouseinslot["equippedSlot"] == "helmet" == self.selected_item:
                screen.blit((self.selected), (self.coo_helmet))
            screen.blit(itimg, (self.coo_helmet))

        # display of inventory completion
        if self.char:
            self.volume = self.get_volume(self.char["Str"])
        screen.blit(
            font.render(
                "inventory completion : "
                + str(round(self.weight))
                + "/"
                + str(self.volume),
                True,
                text_col,
            ),
            (0, 0),
        )
        # display of the gold
        screen.blit(font.render(str(self.gold), True, text_col), self.coo_gold)

        # display of the informations about the item the mouse shows

        line = 0
        if self.infoit is not None:
            # variables usefull to display all the inforamtions
            if self.mouse_position[0] > self.xlimit:
                xlag = -70
            else:
                xlag = 0
            if self.mouse_position[1] > self.ylimit:
                ylag = -120
            else:
                ylag = 0

            if self.selected_item is not None and self.selected_item == self.item_pos:
                y_pos = 1
            else:
                y_pos = 0
            self.fontbackground = pg.transform.scale(
                self.fontbackground, (300, 50 * (y_pos + len(self.infoit)))
            )
            screen.blit(
                self.fontbackground,
                (
                    self.mouse_position[0] + self.gapitinfo + xlag,
                    self.mouse_position[1] + ylag,
                ),
            )
            for param in self.infoit:
                screen.blit(
                    font.render(
                        param + " : " + str(self.infoit[param]), True, text_col
                    ),
                    (
                        self.mouse_position[0] + self.gapitinfo + xlag,
                        self.mouse_position[1] + 50 * line + ylag,
                    ),
                )
                line += 1
            if self.selected_item is not None and self.selected_item == self.item_pos:
                if Item(
                    self.liste[self.selected_item].item_id, self.all_item
                ).consumable:
                    screen.blit(
                        font.render('Press "u" to use it', True, text_col),
                        (
                            self.mouse_position[0] + self.gapitinfo + xlag,
                            self.mouse_position[1] + 50 * line + ylag,
                        ),
                    )
                elif (
                    Item(self.liste[self.selected_item].item_id, self.all_item).type
                    != "unusable"
                ):
                    screen.blit(
                        font.render('Press "e" to ekip it', True, text_col),
                        (
                            self.mouse_position[0] + self.gapitinfo + xlag,
                            self.mouse_position[1] + 50 * line + ylag,
                        ),
                    )
        line = 0
        if self.char:
            for param in self.char:
                screen.blit(
                    font.render(param + " : " + str(self.char[param]), True, text_col),
                    (30, 100 + 50 * line),
                )
                line += 1

        # drag and drop
        # and 0 <= self.getSlot2(self.mouse_position[0], self.mouse_position[1] < len(self.liste) ):
        if self.clic:
            if self.helditem is not None:
                screen.blit(
                    self.itimg,
                    (
                        self.mouse_position[0] + self.mouse_offset[0],
                        self.mouse_position[1] + self.mouse_offset[1],
                    ),
                )
            self.drag_and_drop()

        pg.display.flip()

    def event(self):
        """manage event for the inventory"""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit(self)

            self.mouse_position = pg.mouse.get_pos()
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.clic = True
                    self.mouseinslot = {"slot": False, "equippedSlot": False}
            if event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    self.switch_items(self.helditemslot, self.mouse_position)
                    self.helditem = None
                    self.helditemslot = None
                    self.clic = False
                    self.mouseinslot = {"slot": False, "equippedSlot": False}

            elif event.type == pg.MOUSEMOTION:
                if self.clic:
                    self.mouse_position = pg.mouse.get_pos()

            xpos = self.mouse_position[0]
            ypos = self.mouse_position[1]
            self.mouseinslot = self.isinslot(xpos, ypos)
            if self.mouseinslot["slot"] and not self.clic:
                # get the box where the mouse is
                if not self.mouseinslot["equippedSlot"]:
                    y_pos = (ypos - self.ybegin) // self.boxsize
                    x_pos = (xpos - self.xbegin) // self.boxsize
                    # position of the item in the list (self.liste)
                    self.item_pos = self.getslot(x_pos, y_pos)
                if (
                    self.item_pos is not None
                    and (self.liste[self.item_pos] is not None)
                    and 0 <= self.item_pos < len(self.liste)
                    or (self.mouseinslot["equippedSlot"])
                ):
                    if not self.mouseinslot["equippedSlot"]:
                        itemid = Item(self.liste[self.item_pos].item_id, self.all_item)
                        self.infoit = itemid.getinfo()
                    elif (
                        self.stuff_equipped[self.mouseinslot["equippedSlot"]]
                        is not None
                    ):
                        itemid = Item(
                            self.stuff_equipped[self.mouseinslot["equippedSlot"]],
                            self.all_item,
                        )
                        self.infoit = itemid.getinfo()
                    if event.type == pg.MOUSEBUTTONDOWN and event.button != 1:
                        if not self.mouseinslot["equippedSlot"]:
                            self.selected_item = self.item_pos
                        else:
                            self.selected_item = self.mouseinslot["equippedSlot"]
                else:
                    self.infoit = None
                    self.item_pos = None

                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_d:  # press "d" to delete the item
                            self.remove_item(self.item_pos)
                        if event.key == pg.K_e:  # press "e" to equip the item
                            self.equip(self.selected_item)
            else:
                self.infoit = None
                self.item_pos = None

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_i:  # press "i" to close the inventory
                    self.isopen = False
                    pg.display.set_mode((0, 0), pg.FULLSCREEN)
                if event.key == pg.K_e:  # press "e" to equip the selected item
                    self.equip(self.selected_item)
                if event.key == pg.K_u:  # press "u" to use the item
                    self.use(self.selected_item)

    def isinslot(self, xpos, ypos):
        """return True if the position of the mouse is in a slot"""
        if (
            self.xbegin < xpos < self.xbegin + self.nbox * self.boxsize
            and self.ybegin < ypos < self.ybegin + 6 * self.boxsize
        ):
            return {"slot": True, "equippedSlot": False}
        elif self.coo_weapon[0] < xpos < self.coo_weapon[0] + self.boxsize:
            if self.coo_weapon[1] < ypos < self.coo_weapon[1] + self.boxsize:
                return {"slot": True, "equippedSlot": "weapon"}
            elif self.coo_helmet[1] < ypos < self.coo_helmet[1] + self.boxsize:
                return {"slot": True, "equippedSlot": "helmet"}
            elif self.coo_plastron[1] < ypos < self.coo_plastron[1] + self.boxsize:
                return {"slot": True, "equippedSlot": "plastron"}
        return {"slot": False, "equippedSlot": False}

    def getslot(self, col, row):
        """get slot"""
        return col + row * self.nbox

    def getslot2(self, xpos, ypos):
        """xpos and ypos are the coordinates of the mouse"""
        y_pos = (ypos - self.ybegin) // self.boxsize
        x_pos = (xpos - self.xbegin) // self.boxsize
        return x_pos + y_pos * self.nbox

    def equip(self, item_id, pos=None):
        """equip the item item_id"""
        if item_id is None:
            return

        # unequip an item
        elif isinstance(item_id, str):
            if pos is not None:
                if self.liste[pos] is not None:
                    it2 = self.liste[pos].item_id
                    if (
                        self.all_item[it2]["category"]
                        == self.all_item[self.stuff_equipped[item_id]]["category"]
                    ):
                        self.equip(it2)
                else:
                    item = Item(self.stuff_equipped[item_id], self.all_item)
                    if item.type_bonus == "armor":
                        self.char["armor"] -= item.bonus
                    elif item.type_bonus == "damage":
                        self.char["weapon"] -= item.bonus
                    self.liste[pos] = Item(self.stuff_equipped[item_id], self.all_item)
                    self.stuff_equipped[item_id] = None
                    return

            item = Item(self.stuff_equipped[item_id], self.all_item)
            if item.type_bonus == "armor":
                self.char["armor"] -= item.bonus
            elif item.type_bonus == "damage":
                self.char["weapon"] -= item.bonus
            for i in range(len(self.liste)):
                if self.liste[i] is None:
                    self.liste[i] = Item(self.stuff_equipped[item_id], self.all_item)
                    break
            self.stuff_equipped[item_id] = None
            self.selected_item = None
            return

        # equip an item
        item = Item(self.liste[item_id].item_id, self.all_item)
        category = item.type
        equitem = None
        if self.stuff_equipped[category] is not None:
            equitem = Item(self.stuff_equipped[category], self.all_item)
        if item.consumable or category == "unusable":
            return
        self.selected_item = None

        if self.stuff_equipped[category] is not None and equitem is not None:
            if equitem.type_bonus == "armor":
                self.char["armor"] -= equitem.bonus
            elif equitem.type_bonus == "damage":
                self.char["weapon"] -= equitem.bonus
            for i in range(len(self.liste)):
                if self.liste[i] is None:
                    self.liste[i] = Item(self.stuff_equipped[category], self.all_item)
                    break
        self.liste[item_id] = None
        self.stuff_equipped[category] = item.item_id
        if item.type_bonus == "armor":
            self.char["armor"] += item.bonus
        elif item.type_bonus == "damage":
            self.char["weapon"] += item.bonus

    def use(self, item_id):
        """use item """
        self.selected_item = None
        if not item_id:
            return
        item = Item(self.liste[item_id].item_id, self.all_item)
        if item.consumable:
            if item.type_bonus == "heal":
                self.char["hp"] += item.bonus
            # elif item.type_bonus == 'mana':
            #    self.char[""] += item.bonus
            self.remove_item(item_id)

    def drag_and_drop(self):
        """drag and drop item on click"""
        if self.helditem is None:
            xpos, ypos = self.mouse_position[0], self.mouse_position[1]
            y_pos = (ypos - self.ybegin) // self.boxsize
            x_pos = (xpos - self.xbegin) // self.boxsize
            self.mouseinslot = self.isinslot(xpos, ypos)
            if self.mouseinslot["slot"]:
                if (
                    not self.mouseinslot["equippedSlot"]
                    and 0 <= self.getslot(x_pos, y_pos) < len(self.liste)
                    and self.liste[self.getslot2(xpos, ypos)] is not None
                ):
                    self.helditemslot = self.getslot2(xpos, ypos)
                    self.helditem = self.liste[self.helditemslot].item_id
                elif self.mouseinslot["equippedSlot"]:
                    self.helditemslot = self.mouseinslot["equippedSlot"]
                    self.helditem = self.stuff_equipped[self.helditemslot]
                if self.helditem is not None:
                    self.itimg = pg.image.load(
                        path.join(self.img_folder, self.all_item[self.helditem]["img"])
                    ).convert_alpha()
                    self.itimg = pg.transform.scale(
                        self.itimg, (self.imgsize, self.imgsize)
                    )

    def switch_items(self, helditem, mouse_position):
        """allow to switch items in inventory"""
        if self.helditem is None:
            return
        x_pos, y_pos = mouse_position[0], mouse_position[1]
        isinslot = self.isinslot(x_pos, y_pos)
        if not isinslot:
            return

        elif (
            isinslot["equippedSlot"]
            and isinstance(helditem, int)
            and 0 <= helditem < len(self.liste)
        ):
            # the mouse is in an equipped Slot
            item = self.liste[helditem]
            category = isinslot["equippedSlot"]
            if (
                isinstance(helditem, int)
                and self.all_item[item.item_id]["category"] == category
            ):
                self.equip(helditem)
            return
        mouseslot = self.getslot2(mouse_position[0], mouse_position[1])

        if isinstance(helditem, int) and 0 <= mouseslot < len(self.liste):
            # both items are not equipped
            if not 0 <= helditem < len(self.liste):
                return
            self.liste[helditem], self.liste[mouseslot] = (
                self.liste[mouseslot],
                self.liste[helditem],
            )
            return

        elif isinstance(helditem, str) and self.stuff_equipped[helditem] is not None:
            # the selected item is equipped
            if 0 <= mouseslot < len(self.liste):
                self.equip(helditem, mouseslot)

    def get_volume(self, strength):
        """get volume max from inventory"""
        dic = {
            1: 1.5,
            2: 3,
            3: 5,
            4: 6.5,
            5: 8,
            6: 10,
            7: 11.5,
            8: 13,
            9: 15,
            10: 16.5,
            11: 19,
            12: 21.5,
            13: 25,
            14: 29,
            15: 33,
            16: 38,
            17: 43,
            18: 50,
            19: 58,
            20: 66.5,
            21: 76.5,
            22: 86.5,
            23: 100,
            24: 116.5,
            25: 133,
            26: 153,
        }
        if strength <= 26:
            tmp = dic[strength]
        else:
            tmp = 160
        return tmp
