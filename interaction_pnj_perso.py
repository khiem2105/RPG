"""module that manage the interaction with pnj"""
import pygame
from item import Itemlist, Item
import settings

# On initialise pygame


def acheter(self, store, inventory):
    """
    method used to buy item

    Parameters
    ----------
    self : game
        variable game
    store : Store(Inventory)
        what is proposed by the merchant
    inventory : Inventory
        inventory of the player
    """
    shopping = True
    store.gold = inventory.gold
    liste_items = Itemlist()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    while (
        shopping
    ):  # Tant que le joueur fait ses achats (i.e n'a pas appuyé sur escape)
        # Utilisation de la méthode draw de la classe Inventaire
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE] or keys[pygame.K_i]:
                shopping = False
                return
            else:
                # Le magasin étant un inventaire,
                # j'ai repris du code de la classe Inventaire pour détecter l'item
                # sélectionné par le joueur
                store.mouse_position = pygame.mouse.get_pos()
                xpos = store.mouse_position[0]
                ypos = store.mouse_position[1]
                if (
                    store.xbegin < xpos < store.xbegin + store.nbox * store.boxsize
                    and store.ybegin < ypos < store.ybegin + 6 * store.boxsize
                ):
                    y_pos = (ypos - store.ybegin) // store.boxsize
                    x_pos = (xpos - store.xbegin) // store.boxsize
                    item_pos = x_pos + y_pos * store.nbox
                    liste_items = Itemlist()
                    if store.liste[item_pos] is not None:
                        item = Item(store.liste[item_pos].item_id, liste_items.item_list)
                        item.get_price()
                        store.infoIt = item.getinfo()
                        if (
                            event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
                        ):  # Clic gauche pour sélectionner un objet
                            if inventory.gold < item.price:
                                display_message(
                                    self,
                                    "Your gold : "
                                    + str(inventory.gold)
                                    + "         Price : "
                                    + str(item.price),
                                )
                            else:
                                display_message(
                                    self,
                                    "Do you want to buy "
                                    + item.name
                                    + " for "
                                    + str(item.price)
                                    + "\n Y : Yes           N : No",
                                )
                                # On récupère le solde et l'item sélectionné
                                tmp, got_item = transaction(
                                    store, item, inventory.gold, True
                                )
                                inventory.gold += tmp
                                inventory.weight += tmp / 10
                                store.gold = inventory.gold
                                if got_item:
                                    # On ajoute l'item retiré du magasin à l'inventaire
                                    inventory.add_item(got_item.item_id, got_item.stack)
                                    display_message(
                                        self, "Gold : " + str(inventory.gold)
                                    )
                else:
                    store.infoIt = None
        store.draw(screen)


def vendre(self, store, inventory):
    """
    Parameters
    ----------
    self : game
        variable game
    store : Store(Inventory)
        what is proposed by the merchant
    inventory : Inventory
        inventory of the player
    """
    selling = True
    liste_items = Itemlist()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    while selling:  # Tant que le joueur vend des objets (i.e n'a pas appuyé sur escape)
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE] or keys[pygame.K_i]:
                selling = False
            else:
                inventory.mouse_position = pygame.mouse.get_pos()
                xpos = inventory.mouse_position[0]
                ypos = inventory.mouse_position[1]
                if (
                    inventory.xbegin
                    < xpos
                    < inventory.xbegin + inventory.nbox * inventory.boxsize
                    and inventory.ybegin
                    < ypos
                    < inventory.ybegin + 3 * inventory.boxsize
                ):
                    y_pos = (ypos - inventory.ybegin) // inventory.boxsize
                    x_pos = (xpos - inventory.xbegin) // inventory.boxsize
                    item_pos = x_pos + y_pos * inventory.nbox
                    if 0 <= item_pos < len(inventory.liste):
                        if inventory.liste[item_pos]:
                            item = Item(inventory.liste[item_pos].item_id, liste_items.item_list)
                            item.get_price()
                            inventory.infoIt = item.getinfo()
                            if (
                                event.type == pygame.MOUSEBUTTONDOWN
                                and event.button == 1
                            ):  # Clic gauche pour sélectionner un objet
                                display_message(
                                    self,
                                    "Do you want to sell "
                                    + item.name
                                    + " for "
                                    + str(item.price // 2)
                                    + "\n Y : Yes           N : No",
                                )
                                # On récupère le solde et l'item sélectionné

                                tmp, got_item = transaction(
                                    inventory, item, inventory.gold, False
                                )
                                inventory.gold += tmp
                                inventory.weight += tmp / 10
                                if got_item:
                                    # On ajoute l'item retiré de l'inventaire au magasin
                                    store.add_item(got_item.item_id, got_item.stack)
                                    display_message(
                                        self, "Gold : " + str(inventory.gold)
                                    )
        # Utilisation de la méthode draw de la classe Inventaire
        inventory.draw(screen)


def transaction(menu, selected_item, money, buying):
    """
    method that manage the money and the item to add or to remove

    Parameters
    ----------
    menu : Inentory or Store(Inventory)
        if the player is buying, then 'menu' contains the store of the merchant
        if the player is selling, then 'menu' contains the inventory of the player 
    selected_item : Item
        item selected by the player
    money : int
        amount of gold the player has
    buying : boolean
        if the player buys, then 'buying = True' and the value of the item will be debited to the player's gold
        if the player sells, then 'buying = False' and the value of the item will be credited to the player's gold

    """
    transaction_ = True
    while transaction_:
        for new_event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if new_event.type == pygame.KEYDOWN:
                if keys[pygame.K_y]:
                    if buying:  # Si True, le joueur est en train d'acheter :
                        # il est débité. Sinon, il est crédité
                        money = -selected_item.price
                    else:
                        if selected_item.price == 1:
                            money = 1
                        else:
                            money = selected_item.price // 2
                    got_item = selected_item
                    # Méthode remove de la classe Inventory
                    selected_item.stack -= 1
                    if selected_item.stack == 0:
                        menu.remove_item(selected_item)
                    transaction_ = False
                    return (money, got_item)
                elif keys[pygame.K_n]:
                    transaction_ = False
                    return (money, None)


def display_message(self, message):
    """
    method to generate

    Parameters
    ----------
    self : game
        variable game
    message : str
        message which will be displayed
    """
    police = pygame.font.SysFont("Cascadia code", 50)
    textrect = pygame.Rect(0, 0, settings.WIDTH, 2 * settings.TILESIZE)
    textrect.center = ((settings.WIDTH / 2), (settings.HEIGHT - textrect.height))
    x_pos, y_pos = (textrect.left + 5 * settings.TILESIZE), (textrect.top)
    pygame.draw.rect(self.screen, settings.BLACK, textrect)
    for ligne in message.splitlines():
        x_pos, y_pos = self.screen.blit(
            police.render(ligne, 1, settings.WHITE), (x_pos, y_pos)
        ).bottomleft

    pygame.display.update(textrect)
    pygame.time.delay(500)
