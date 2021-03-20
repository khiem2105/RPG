import pygame as pg
import settings
from sprites import Tile, MMap
from store import Store
from box import Button
from os import path
import csv


class Pnj(Tile):
    """
    A class used to select and change the different values of the character's abilities

    Attributes
    ----------
    self.is_merchant : boolean
        specifies if the PNJ is a merchant
    self.has_quest : dictionnary
        contains all informations about the quest attributed by this PNJ
    self.quest_id : int
        number of the quest (it is between 0 and 7)
    self.solving_quest
        specifies if the player is currently solving the quest attributed by this PNJ
    self.store : class Store(Inventory)
        if the PNJ is a merchant, contains the items which can be bought by the player
    self.quest 
    self.talking : pygame.Surface
        display surface for the speeches of the PNJ
    self.game : class Game
        the variable game
    self.level_number : int
        number of the level of the game
    self.pnj_id : int
        identification number of the PNJ
    self.text : dict
        dialogues of the PNJ according to the context
        
    pnj_folder : str
        name of the folder containing the images of the PNJ
    

    Methods
    -------
    self.attribute_quest(game)
        attributes the quest to the PNJ according to the document "pnj_data.csv"
    self.set_img_name(game)
        explicites what is the name of the picture of the PNJ
    self.load_text()
        fill in the dictionary "self.text"
    self.talk()
        initializes the surface and the buttons which will be used to interact with the PNJ
    self.update()
        resets all variables dedicated to the discussion with the PNJ
    

    """
    def __init__(self, game, x, y, is_merchant):
        """
        Parameters
        ----------
       game : Game
            variable game
        x, y : float
            position of the PNJ on the map
        is_merchant
            specifies if the PNJ has to be a merchant
        """
        super().__init__(game, x, y)
        self.is_merchant = is_merchant
        self.has_quest = None
        self.quest_id = None
        self.solving_quest = False
        self.node.make_barrier()
        self.store = None
        self.quest = False
        self.talking = None
        self.game = game
        self.level_number = game.current_level
        self.pnj_id = 0
        self.text = {}
        if not game.editor:
            self.has_quest = None
            self.quest_id = None
            self.solving_quest = False
            self.node.make_barrier()
            self.store = None
            self.quest = False
            self.talking = None
            self.talking_pos = None
            self.pnj_id = len(game.sprites[game.current_level]["J"]) + len(
                game.sprites[game.current_level]["M"]
            )
            # S'il n'y a aucun PNJ dans game.sprites, le pnj prend id = 0
            # Le suivant prend 1, le suivant 2...
            # Le numéro tient compte des PNJ lambda et des marchands déjà stockés dans game.sprites,
            # car il n'est pas exclu que les marchands puissent proposer des quêtes
            # auquel cas on aura besoin d'un numéro unique par PNJ

            if self.is_merchant:
                self.store = Store(game, self.pnj_id, {})
        pnj_folder = path.join(game.game_folder, "img")
        if self.is_merchant:
            self.image = pg.image.load(path.join(pnj_folder, game.img_path["M"]))
        else:
            self.image = pg.image.load(path.join(pnj_folder, game.img_path["J"]))
        if not game.editor:
            self.attribute_quest(game)
            self.set_img_name(game)
            self.load_text()

    def attribute_quest(self, game):
        """
        attributes the quest to the PNJ according to the document "pnj_data.csv"

        Parameters
        ----------
        game : Game
            variable game
        """
        game_folder = path.dirname(__file__)
        pnj_data = path.join(game_folder, "data/pnj_data.csv")
        pnj_file = open(pnj_data)
        reader = csv.reader(pnj_file, delimiter=";")
        next(reader)
        for perso in reader:
            if (self.level_number == int(perso[0])) and (self.pnj_id == int(perso[1])):
                self.has_quest = game.quest.quest_list[perso[3]]
                self.quest_id = int(perso[3])
                print(type(self.has_quest), type(self.quest_id))

    def set_img_name(self, game):
        """
        explicites what is the name of the picture of the PNJ

        Parameters
        ----------
        game : Game
            variable game
        """
        game_folder = path.dirname(__file__)
        pnj_data = path.join(game_folder, "data/pnj_data.csv")
        pnj_file = open(pnj_data)
        pnj_folder = path.join(path.join(game_folder, "img"), "pnj")
        reader = csv.reader(pnj_file, delimiter=";")
        next(reader)
        for perso in reader:
            if (self.level_number == int(perso[0])) and (self.pnj_id == int(perso[1])):
                self.image = pg.image.load(
                    path.join(pnj_folder, perso[2])
                ).convert_alpha()
                break
            else:
                if self.is_merchant:
                    self.image = pg.image.load(
                        path.join(pnj_folder, game.img_path["M"])
                    )
                else:
                    self.image = pg.image.load(
                        path.join(pnj_folder, game.img_path["J"])
                    )
        self.image = pg.transform.scale(
            self.image, (settings.TILESIZE, settings.TILESIZE)
        )

    def load_text(self):
        """
            fill in the dictionary "self.text"
        """
        game_folder = path.dirname(__file__)
        pnj_data = path.join(game_folder, "data/pnj_data.csv")
        pnj_file = open(pnj_data)
        reader = csv.reader(pnj_file, delimiter=";")
        next(reader)
        for perso in reader:
            if (self.level_number == int(perso[0])) and (self.pnj_id == int(perso[1])):
                self.text["Before quest"] = perso[4]
                self.text["During quest"] = perso[5]
                self.text["Fulfilled quest"] = perso[6]
        self.text["No story"] = "I have no quest for you"

    def talk(self):
        """
            initializes the surface and the buttons which will be used to interact with the PNJ
        """
        self.talking = pg.Surface((175, 350), pg.SRCALPHA, 32)
        if not self.talking_pos:
            self.talking_pos = (
                settings.WIDTH // 2 - self.talking.get_rect().width // 2,
                settings.HEIGHT // 2 - self.talking.get_rect().height // 2,
            )
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, "img")
        self.talking.blit(pg.image.load(path.join(img_folder, "loot.png")), (0, 0))
        if self.is_merchant:
            self.game.buttons.clear()
            _ = pg.font.SysFont("cascadia code", 40).render("Buy", True, (204, 153, 51))
            self.talking.blit(
                _, (self.talking.get_rect().width // 2 - _.get_rect().width // 2, 60)
            )
            self.game.buttons["buy"] = Button(
                self.talking_pos[0] + 12,
                self.talking_pos[1] + 55,
                (self.talking.get_rect().width - 25, 30),
            )
            _ = pg.font.SysFont("cascadia code", 40).render(
                "Sell", True, (204, 153, 51)
            )
            self.talking.blit(
                _, (self.talking.get_rect().width // 2 - _.get_rect().width // 2, 120)
            )
            self.game.buttons["sell"] = Button(
                self.talking_pos[0] + 12,
                self.talking_pos[1] + 115,
                (self.talking.get_rect().width - 25, 30),
            )
        if self.has_quest:
            _ = pg.font.SysFont("cascadia code", 40).render(
                "Quest", True, (204, 153, 51)
            )
            self.talking.blit(
                _,
                (self.talking.get_rect().width // 2 - _.get_rect().width // 2, 180),
            )
            self.game.buttons["quest"] = Button(
                self.talking_pos[0] + 12,
                self.talking_pos[1] + 175,
                (self.talking.get_rect().width - 25, 30),
            )

    def update(self):
        """
            resets all variables dedicated to the discussion with the PNJ
        """
        if not self.game.editor:
            if self.game.player.inmovement:
                self.talking = None
                self.talking_pos = None
                self.quest = False
                self.game.log["pnj"] = None
