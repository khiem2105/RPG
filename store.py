from inventory import Inventory
from item import Itemlist
import random


class Store(Inventory):
    def __init__(self, game, merchant_id, dic_char, dic_inv=None, volume=100, pnj=True):
        super().__init__(game, dic_char, dic_inv, volume, True)
        self.merchant_id = merchant_id
        self.sum_rarity = 0  # Somme de la rareté de tous les items
        # self.sum_rarity devra se situer dans cet intervalle
        self.sum_rarity_limits = (900, 1000)
        self.color = (35, 85, 30)

        init_item = Itemlist()

        while self.sum_rarity <= self.sum_rarity_limits[0]:
            rand = random.randint(0, 27)
            rarity = init_item.item_list[rand]["rarity"]
            if (
                rarity < 100
            ):  # évite d'ajouter des items de rareté 100, car ce sont des objets prévus pour les quêtes
                self.add_item(rand)
                self.sum_rarity += rarity
