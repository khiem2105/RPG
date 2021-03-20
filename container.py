"""Module that contains Container class"""
from os import path
import pygame
from pygame.locals import *
from sprites import Tile, MMap
from item import Item
from combat_log import Log
import settings


class Container(Tile):
    """
    class that manages Container

    Attributes
    ----------
    self.map : MMap
        adds the container to game.mmap_group    
    self.opened : boolean
        specifies if the container is already opened or not
    self.stashed_item : Item
        item stashed by the container
    self.screen_surface : pygame.Surface
        used to print informations when the player tries to open the container
    self.screen_pos : tuple
        position of the self.screen_surface

    game_folder : str
        current folder name
    img_folder : str
        name of the folder containing the picture of the container
    self.screen_bubble : str
        background image where the text is printed
    

    Methods
    -------
    self.open
        defines if the player is allowed to open the container, and sets self.opened and game.log["container"] in consequence
    self.blit_container
        sets self.screen_pos and self.screen_surface, needed to print the informative text 
    self.container_update
        resets self.screen_surface and game.log["container"]
    
    

    """

    def __init__(self, game, x, y):
        """
        Parameters
        ----------
        game : Game
            variable game
        x, y : float
            position of the container on the map
        """
        super().__init__(game, x, y)
        self.map = MMap(game, x, y, game.m_img["C"])
        self.node.make_barrier()
        self.image = game.img["C"]
        self.opened = False
        self.stashed_item = Item(8, game.all_item)
        self.screen_surface = None
        self.screen_pos = None

        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, "img")
        self.screen_bubble = pygame.image.load(path.join(img_folder, "loot.png")).convert_alpha()
    
    def open(self, game):
        """
        defines if the player is allowed to open the container, and sets self.opened and game.log["container"] in consequence
        
        Parameters
        ----------
        game : Game
            variable game
        """
        position = (pygame.mouse.get_pos()[0] + 5, pygame.mouse.get_pos()[1] + 10)               
        game.log["container"] = Log(
            170, 340, position, settings.WHITE, 26, game, combat=False, quest=True
        )
        if self.opened:
            game.log["container"].add_log("Container already opened")
        else:
            has_key = False
            for item in game.player.inventory.liste:
                if item:
                    if item.item_id == 43:
                        has_key = True
                        break

            if has_key:
                game.log["container"].add_log("Congratulations! You got the blacksmith's hammer")
                self.opened = True
                game.player.inventory.add_item(self.stashed_item.item_id)
                self.stashed_item = None
            else:
                game.log["container"].add_log("You don't have key")
        self.blit_container()


    def blit_container(self):
        """
        sets self.screen_pos and self.screen_surface, needed to print the informative text 
        """
        self.screen_pos = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        self.screen_surface = pygame.Surface((175, 350), pygame.SRCALPHA, 32)

    def container_update(self, game):
        """
        resets self.screen_surface and game.log["container"]

        Parameters
        ----------
        game : Game
            variable game
        """
        self.screen_surface = None
        game.log["container"] = None       
