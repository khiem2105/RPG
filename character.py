"""Module that contains Character class"""


class Character:
    """
    A class to manage characters

    Attrinutes
    ----------
    name : str
        name of the character
    _class : str
        class of the character
    hp : int
        value of the character's life points
    xp : int
        value of the character's experience
    Str : int
        value of the character's strenght
    Int : int
        value of the character's intelligence
    Wis : int
        value of the character's wisdom
    Cha : int
        value of the character's charisma
    Con : int
        value of the character's constitution
    Dex : int
        value of the character's dexterity
    armor : int
        value of the character's armor
    level : int
        value of the character's current level

    Methods
    -------
    damage(dm)
        soustract the damage points to the character's hp/life points value
    win_xp(xp)
        add xp to the actual character's xp value
    improve_skill(skill,n)
        add n to the value of the choosen skill (ability)
    improve_level()
        improve the character's level and set the xp's value to zero
    save()
        return a dictionary with all the informations about the character
    """

    def __init__(
        self,
        name,
        _class,
        hp,
        xp,
        Str,
        Con,
        Dex,
        Int,
        Wis,
        Cha,
        armor,
        weapon,
        level,
        carac_point,
    ):
        """
        Parameters
        ----------
        name : str
            name of the character
        _class : str
            class of the character
        hp : int
            value of the character's life points
        xp : int
            value of the character's experience
        Str : int
            value of the character's strenght
        Int : int
            value of the character's intelligence
        Wis : int
            value of the character's wisdom
        Cha : int
            value of the character's charisma
        Con : int
            value of the character's constitution
        Dex : int
            value of the character's dexterity
        armor : int
            value of the character's armor
        level : int
            value of the character's current level
        """
        self.name = name
        self._class = _class
        self.health = hp
        self.exp = xp
        self.str = Str
        self.int = Int
        self.wis = Wis
        self.cha = Cha
        self.con = Con
        self.dex = Dex
        self.armor = armor
        self.weapon = weapon
        self.level = level
        self.carac_point = carac_point
        self.dic_ab = None

    def damage(self, dmg):
        """soustract the damage points to the character's hp/life points value

        Parameters
        ----------
        dm : int
            value of the receive damages
        """
        self.health -= dmg

    def win_xp(self, exp):
        """add xp to the actual character's xp value

        Parameters
        ----------
        xp : int
            value of the added xp
        """
        self.exp += exp

    def improve_skill(self, skill, nmb):
        """add n to the value of the choosen skill (ability)

        Parameters
        ----------
        skill : str
            skill that has to be improved
        n : int
            value added to the actual skill value
        """
        if skill == "Str":
            self.str += nmb
        elif skill == "Con":
            self.con += nmb
        elif skill == "Int":
            self.int += nmb
        elif skill == "Wis":
            self.wis += nmb
        elif skill == "Dex":
            self.dex += nmb
        elif skill == "Cha":
            self.cha += nmb

    def improve_level(self):
        """improve the character's level and set the xp's value to zero"""
        self.level += 1
        self.exp = 0

    def save(self):
        """return a dictionary with all the informations about the character"""
        save_object = {
            "name": self.name,
            "class": self._class,
            "Str": self.str,
            "Con": self.con,
            "Int": self.int,
            "Wis": self.wis,
            "Dex": self.dex,
            "Cha": self.cha,
            "armor": self.armor,
            "weapon": self.weapon,
            "xp": self.exp,
            "hp": self.health,
            "level": self.level,
            "carac point": self.carac_point,
            "dic_Ab": self.dic_ab,
        }

        return save_object


class Wizard(Character):
    """
    A class used to manage wizards

    Attributes
    ----------
    dic_Ab : dict
        dictionary containing the name of the different skills used by a wizard
    spells : dict
        spells that can be used by wizards
    """

    def __init__(
        self,
        name,
        _class,
        hp,
        xp,
        Str,
        Con,
        Dex,
        Int,
        Wis,
        Cha,
        armor,
        weapon,
        level=1,
        carac_point=0,
    ):
        super().__init__(
            name,
            _class,
            hp,
            xp,
            Str,
            Con,
            Dex,
            Int,
            Wis,
            Cha,
            armor,
            weapon,
            level,
            carac_point,
        )
        self.dic_ab = {
            "Str": "",
            "Con": "",
            "Int": "Craft",
            "Wis": "Profession",
            "Dex": "Fly",
            "Cha": "",
            "Armor": "",
            "Weapon": "",
        }


class Barbarian(Character):
    """
    A class used to manage barbarians

    Attributes
    ----------
    dic_Ab : dict
        dictionary containing the name of the different skills used by a barbarian
    """

    def __init__(
        self,
        name,
        _class,
        hp,
        xp,
        Str,
        Con,
        Dex,
        Int,
        Wis,
        Cha,
        armor,
        weapon,
        level=1,
        carac_point=0,
    ):
        super().__init__(
            name,
            _class,
            hp,
            xp,
            Str,
            Con,
            Dex,
            Int,
            Wis,
            Cha,
            armor,
            weapon,
            level,
            carac_point,
        )
        self.dic_ab = {
            "Str": "Climb",
            "Con": "",
            "Int": "Craft",
            "Wis": "Survival",
            "Dex": "Ride",
            "Cha": "Intimidate",
            "Armor": "",
            "Weapon": "",
        }


class Rogue(Character):
    """
    A class used to manage rogues

    Attributes
    ----------
    dic_Ab : dict
        dictionary containing the name of the different skills used by a rogue
    """

    def __init__(
        self,
        name,
        _class,
        hp,
        xp,
        Str,
        Con,
        Dex,
        Int,
        Wis,
        Cha,
        armor,
        weapon,
        level=1,
        carac_point=0,
    ):
        super().__init__(
            name,
            _class,
            hp,
            xp,
            Str,
            Con,
            Dex,
            Int,
            Wis,
            Cha,
            armor,
            weapon,
            level,
            carac_point,
        )
        self.dic_ab = {
            "Str": "Climb",
            "Con": "",
            "Int": "Appraise",
            "Wis": "Perception",
            "Dex": "Escape Artist",
            "Cha": "Bluff",
            "Armor": "",
            "Weapon": "",
        }
