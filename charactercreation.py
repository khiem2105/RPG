"""just a method"""
import character


class Creation:
    """
    A class used to create the character according to its class
    """

    def creation_perso(self, name, _class, portrayal, dic_ab, menu):
        """allow to create the character according to its class

        Parameters
        ----------
        name : str
            character's name
        _class : str
            character's class
        portrayal : str
            name of the image used to the character's portrayal
        dic_ab : dict
            dictionary that contains all the caracteristics of the character
        menu : creation_menu
            menu used to create the character;allow to complete some empty
            fields (portrayal_name_img and chara_create)
        """
        if _class == "Wizard":
            player = character.Wizard(
                name,
                _class,
                0,
                0,
                dic_ab["Str"],
                dic_ab["Con"],
                dic_ab["Dex"],
                dic_ab["Int"],
                dic_ab["Wis"],
                dic_ab["Cha"],
                0,
                0,
            )
            menu.chara_create["Wizard"]["dic"] = player.save()
            menu.chara_create["Wizard"]["portrayal_name_img"] = portrayal
            menu.close()
        elif _class == "Barbarian":
            player = character.Barbarian(
                name,
                _class,
                0,
                0,
                dic_ab["Str"],
                dic_ab["Con"],
                dic_ab["Dex"],
                dic_ab["Int"],
                dic_ab["Wis"],
                dic_ab["Cha"],
                0,
                0,
            )

            menu.chara_create["Barbarian"]["dic"] = player.save()
            menu.chara_create["Barbarian"]["portrayal_name_img"] = portrayal
            menu.close()
        elif _class == "Rogue":
            player = character.Rogue(
                name,
                _class,
                0,
                0,
                dic_ab["Str"],
                dic_ab["Con"],
                dic_ab["Dex"],
                dic_ab["Int"],
                dic_ab["Wis"],
                dic_ab["Cha"],
                0,
                0,
            )

            menu.chara_create["Rogue"]["dic"] = player.save()
            menu.chara_create["Rogue"]["portrayal_name_img"] = portrayal
            menu.close()
