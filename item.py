"""module that manage item_list and item class"""
import csv
from os import path


class Itemlist:
    """list of all the item from the game"""

    def __init__(self):
        game_folder = path.dirname(__file__)
        data_item = path.join(game_folder, r"data\data_item.csv")
        file_item = open(data_item)
        reader = csv.reader(file_item, delimiter=";")
        self.item_list = {}

        next(reader)
        for raw in reader:
            item_id = int(raw[0])
            name = raw[1]
            img = raw[2]
            weight = int(raw[3])
            category = raw[4]
            type_bonus = raw[5]
            bonus = raw[6]
            if raw[7] == "y":
                consumable = True
            else:
                consumable = False
            rarity = int(raw[8])
            stack = raw[9]
            self.item_list[item_id] = {
                "name": name,
                "img": img,
                "weight": weight,
                "category": category,
                "type_bonus": type_bonus,
                "bonus": bonus,
                "consumable": consumable,
                "stack": int(stack),
                "rarity": rarity,
            }
        file_item.close()


class Item:
    """class item"""

    def __init__(self, item_id, item_list, stack=None):
        self.weight = item_list[item_id]["weight"]
        # id is an integer to recognise the item
        self.item_id = item_id
        # img is the sprite of the item
        self.img = item_list[item_id]["img"]
        self.name = item_list[item_id]["name"]
        self.type = item_list[item_id]["category"]
        self.type_bonus = item_list[item_id]["type_bonus"]
        self.bonus = int(item_list[item_id]["bonus"])
        self.consumable = item_list[item_id]["consumable"]
        self.rarity = item_list[item_id]["rarity"]
        self.price = 0
        if stack:
            self.stack = stack
        else:
            self.stack = 1
        self.max_stack = item_list[item_id]["stack"]
        self.get_price()

    def getinfo(self):
        """getinfo from the item"""
        return {
            "name": self.name,
            "weight": self.weight,
            "type": self.type,
            self.type_bonus: self.bonus,
            "price": self.price,
        }

    def get_price(self):
        """get price for the item"""
        self.price = self.rarity
