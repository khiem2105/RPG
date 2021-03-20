""" A module used to select and change the different values of the character's abilities"""


class Ability:
    """
    A class used to select and change the different values of the character's abilities

    Attributes
    ----------
    _class : str
        current class associated with the Ability object
    Points : int
        number of remaining points to change/improve abilities' value
    dic_ab : dict
        value of the different character's abilities
    add_functions : dict
        allow to call the good fonction to increment the value of the choosen ability
    sub_functions : dict
        allow to call the good fonction to decrement the value of the choosen ability

    Methods
    -------
    initialised_dic_ab ()
        give the abilities' default values according to the class
    resetAbility ()
        the character's abilities are set on their default value according to the class
    add_ability(Ability)
        indicate if the ability's value can be increased
    sub_ability(Ability)
        indicate if the ability's value can be decreased
    characteristics_add_str () / characteristics_sub_str ()
        increment or decrement the value of the character's ability "str"
    characteristics_add_dex () / characteristics_sub_dex ()
        increment or decrement the value of the character's ability "dex"
    characteristics_add_con () / characteristics_sub_con ()
        increment or decrement the value of the character's ability "con"
    characteristics_add_int () / characteristics_sub_int ()
        increment or decrement the value of the character's ability "int"
    characteristics_add_wis () / characteristics_sub_wis ()
        increment or decrement the value of the character's ability "wis"
    characteristics_add_cha () / characteristics_sub_cha ()
        increment or decrement the value of the character's ability "cha"
    """

    def __init__(
        self,
        _class,
        dic_ab=None,
        points=0,
):
        """
        Parameters
        ----------
        _class : str
            current class associated with the Ability object
        dic_ab : dict, optional
            value of the different character's abilities (None to use the default one associated with the class)
        points : int, optional
            number of remaining points to change/improve abilities' value (default value is 0, used with the default values of dic_ab)
        """
        self._class = _class
        self.points = points
        if not dic_ab:
            self.dic_ab = self.initialised_dic_ab ()
        else:
            self.dic_ab = dic_ab

        self.add_functions = {
            "Str": self.characteristics_add_str,
            "Dex": self.characteristics_add_dex,
            "Con": self.characteristics_add_con,
            "Int": self.characteristics_add_int,
            "Wis": self.characteristics_add_wis,
            "Cha": self.characteristics_add_cha,
        }

        self.sub_functions = {
            "Str": self.characteristics_sub_str,
            "Dex": self.characteristics_sub_dex,
            "Con": self.characteristics_sub_con,
            "Int": self.characteristics_sub_int,
            "Wis": self.characteristics_sub_wis,
            "Cha": self.characteristics_sub_cha,
        }

    def initialised_dic_ab (self):
        """give the abilities' default values according to the class"""

        dic_class={"Wizard":{'Str':10,'Dex':11, 'Con':12,'Int':15,'Wis':13,'Cha':12},
        "Barbarian":{'Str':17,'Dex':10, 'Con':12,'Int':10,'Wis':10,'Cha':10}, 
        "Rogue":{'Str':15,'Dex':14, 'Con':13,'Int':12,'Wis':10,'Cha':8}}
        return dic_class[str(self._class)]

    def reset_ability(self):
        """the character's abilities are set on their default value according to the class"""

        dic_class={"Wizard":{'Str':10,'Dex':11, 'Con':12,'Int':15,'Wis':13,'Cha':12},
        "Barbarian":{'Str':17,'Dex':10, 'Con':12,'Int':10,'Wis':10,'Cha':10}, 
        "Rogue":{'Str':15,'Dex':14, 'Con':13,'Int':12,'Wis':10,'Cha':8}}
        self.dic_ab=dic_class[self._class]
        self.points = 0

    def add_ability(self, ability):
        """indicate if the ability's value can be increased

        Parameters
        ----------
        Ability : int
            value of the current choosen ability
        """

        # mode standard fantasy: Points<=15 -> 18 ne sera jamais utilisé dans ce mode
        verifpoints = {
            "7": -4,
            "8": -2,
            "9": -1,
            "10": 0,
            "11": 1,
            "12": 2,
            "13": 3,
            "14": 5,
            "15": 7,
            "16": 10,
            "17": 13,
            "18": 17,
        }

        if (
            8 <= ability + 1 <= 18
            and self.points + verifpoints[str(ability)] - verifpoints[str(ability + 1)]
            >= 0
        ):
            self.points = (
                self.points + verifpoints[str(ability)] - verifpoints[str(ability + 1)]
            )
            return True
        return False

    def sub_ability(self, ability):
        """indicate if the ability's value can be decreased

        Parameters
        ----------
        Ability : int
            value of the current choosen ability
        """

        verifpoints = {
            "7": -4,
            "8": -2,
            "9": -1,
            "10": 0,
            "11": 1,
            "12": 2,
            "13": 3,
            "14": 5,
            "15": 7,
            "16": 10,
            "17": 13,
            "18": 17,
        }

        if (
            7 <= ability - 1 <= 17
            and self.points + verifpoints[str(ability)] - verifpoints[str(ability - 1)]
            > 0
        ):
            self.points = (
                self.points + verifpoints[str(ability)] - verifpoints[str(ability - 1)]
            )
            return True
        return False

    def characteristics_add_str(self):
        """increment the value of the character's ability "str" """

        if self.add_ability(self.dic_ab["Str"]):
            self.dic_ab["Str"] += 1

    def characteristics_sub_str(self):
        """decrement the value of the character's ability "str" """

        if self.sub_ability(self.dic_ab["Str"]):
            self.dic_ab["Str"] -= 1

    def characteristics_add_dex(self):
        """increment the value of the character's ability "dex" """

        if self.add_ability(self.dic_ab["Dex"]):
            self.dic_ab["Dex"] += 1

    def characteristics_sub_dex(self):
        """decrement the value of the character's ability "dex" """

        if self.sub_ability(self.dic_ab["Dex"]):
            self.dic_ab["Dex"] -= 1

    def characteristics_add_con(self):
        """increment the value of the character's ability "con" """

        if self.add_ability(self.dic_ab["Con"]):
            self.dic_ab["Con"] += 1

    def characteristics_sub_con(self):
        """decrement the value of the character's ability "con" """

        if self.sub_ability(self.dic_ab["Con"]):
            self.dic_ab["Con"] -= 1

    def characteristics_add_int(self):
        """increment the value of the character's ability "int" """

        if self.add_ability(self.dic_ab["Int"]):
            self.dic_ab["Int"] += 1

    def characteristics_sub_int(self):
        """decrement the value of the character's ability "int" """

        if self.sub_ability(self.dic_ab["Int"]):
            self.dic_ab["Int"] -= 1

    def characteristics_add_wis(self):
        """increment the value of the character's ability "wis" """

        if self.add_ability(self.dic_ab["Wis"]):
            self.dic_ab["Wis"] += 1

    def characteristics_sub_wis(self):
        """decrement the value of the character's ability "wis" """

        if self.sub_ability(self.dic_ab["Wis"]):
            self.dic_ab["Wis"] -= 1

    def characteristics_add_cha(self):
        """increment the value of the character's ability "cha" """

        if self.add_ability(self.dic_ab["Cha"]):
            self.dic_ab["Cha"] += 1

    def characteristics_sub_cha(self):
        """decrement the value of the character's ability "cha" """

        if self.sub_ability(self.dic_ab["Cha"]):
            self.dic_ab["Cha"] -= 1

    def get_ability(self):
        """getter for ability dic"""
        return self.dic_ab
