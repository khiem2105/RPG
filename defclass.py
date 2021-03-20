"""Module that contains DefClass class"""
from os import path, listdir
from random import randint


class DefClass:
    """
    A class used to select/change the character's class and associate a portrayal

    Attributes
    ----------
    class_id : int
        number of the class
    name_class : list
        list of the different classes
    portrayal : str
        name of the image used for the portrayal

    Methods
    -------
    set_class_next ()
        change the value of "class_id" to go to the next class,
         and modified the portrayal according to the new class
    set_class_prev ()
        change the value of "class_id" to go to the previous class,
         and modified the portrayal according to the new class
    get_class ()
        give the name of the current class
    choose_portrayal()
        return the name of the image choosen (at random) in an "image bank"
        according to the current class
    """

    def __init__(self, menu):
        """
        Parameters
        ----------
        menu : creation_menu
            menu used to create the character;allow to save what was entered to the associated class
        """

        self.class_id = 0
        self.name_class = ["Barbarian", "Wizard", "Rogue"]
        self.portrayal = self.choose_portrayal()
        self.menu = menu

    def set_class_next(self):
        """change the value of "class_id" to go to the next class,
        and modified the portrayal according to the new class"""
        self.menu.save_before_change()
        self.class_id = (self.class_id + 1) % len(self.name_class)
        self.portrayal = self.choose_portrayal()
        self.save_class()

    def set_class_prev(self):
        """change the value of "class_id" to go to the previous class,
        and modified the portrayal according to the new class"""
        self.menu.save_before_change()
        self.class_id = (self.class_id - 1) % len(self.name_class)
        self.portrayal = self.choose_portrayal()
        self.save_class()

    def get_class(self):
        """give the name of the current class"""
        return self.name_class[self.class_id]

    def choose_portrayal(self):
        """return the name of the image choosen (at random) in an "image bank"
        according to the current class"""
        game_folder = path.dirname(__file__)
        img_folder = path.join(
            game_folder, "img\\" + "portrayal_bank\\" + self.get_class()
        )
        list_portrayal = listdir(img_folder)
        random_portrayal = randint(0, len(list_portrayal) - 1)
        # permet de trouver le portrait associé au numéro tiré au hasard
        return list_portrayal[random_portrayal]

    def save_class(self):
        """function that save class"""
        self.menu.change_current_ab()
