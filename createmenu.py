"""Module that contains CreationMenu class"""
from os import path
import pygame
from defclass import DefClass
from ability import Ability
from inputBox import InputBox
from abilitycontrol import AbilityControl
from classcontrol import ClassControl
from button import Button
from charactercreation import Creation
from menucolors import Menu_colors


class CreationMenu:

    """
    A class to display the creation menu on the screen

    Attributes
    ----------
    game_folder : str
            give the path of the current directory
    img_folder : str
        give the path to access to the "img" directory
    font_folder : str
        give the path to access to the "font" directory
    imgfont : Surface
        the surface where the menu's font image is displayed
    gameDisplay : Surface
        initialize a window/screen to display.
        The created surface will have the same size as the current screen resolution
    display_width : int
        width of the window/surface
    display_height : int
        height of the window/surface
    clock : Clock
        to track time within the game
    count : int
        count how many character are saved
    active : boolean
        inform if the screen menu must be display or not
    chara_create : dict
        dictionary that contains all the caracteristics of the new characters
    dic_ab_class : dict
        contain all the informations about the characters created in the three different classes
    current_class : def_class
        the current class
    current_Ab : Ability
        the current abilities that are displayed and
        can be modified (associated to the current class)
    current_name : str
        name of the current character (associated to the current class)
    seen : list [str]
        indicate which class was visited/seen by the user
    portrayal_name_img : str
        name of the image used for the portrayal


    Methods
    -------
    main ()
        call all the methods to display the creation menu's buttons,
        inputbox, texts and dictionnaries that will be necessary to the
        character's creation
    quitGame()
        quit/close the window
    Aff_text(msg, size, X, Y, display : pygame.Surface)
        allow to display the message with a specific size on a
        screen according to the X and Y coordinates
    initialised ()
        Allow to initialised the abilities' dictionnary
    save_before_change ()
        Allow to save/stock the values associated to the current class
    change_current_Ab ()
        Allow to change the current class and display the good associated values/informations
    allseen()
        indicate if all the characters were seen by the user
    close ()
        Allow to close the window/stop to display the creation menu when
        the characters/three classes are saved
    """

    def __init__(self):

        self.game_folder = path.dirname(__file__)
        self.img_folder = path.join(self.game_folder, "img")
        self.imgfont = pygame.image.load(
            path.join(self.img_folder, "img_menu_rules___character_creation.png")
        )
        self.font_folder = path.join(self.game_folder, "font")

        self.gamedisplay = pygame.display.set_mode(
            (0, 0), pygame.FULLSCREEN
        )  # fullscreen
        (
            self.display_width,
            self.display_height,
        ) = pygame.display.get_surface().get_size()

        self.clock = pygame.time.Clock()
        self.count = 0
        self.active = True
        self.chara_create = {"Wizard": dict(), "Barbarian": dict(), "Rogue": dict()}
        self.dic_ab_class = {
            "Wizard": {
                "Ab": self.initialised("Wizard"),
                "portrayal_name_img": None,
                "Name": "Kadgar",
            },
            "Barbarian": {
                "Ab": self.initialised("Barbarian"),
                "portrayal_name_img": None,
                "Name": "Garrosh",
            },
            "Rogue": {
                "Ab": self.initialised("Rogue"),
                "portrayal_name_img": None,
                "Name": "Valeera",
            },
        }

        self.current_class = DefClass(self)  # indicate the current class
        self.current_ab = Ability(
            self.current_class.get_class(),
            self.dic_ab_class[self.current_class.get_class()]["Ab"]["dic_Ab"],
            self.dic_ab_class[self.current_class.get_class()]["Ab"]["Points"],
        )  # give the abilities associated with the current class
        self.current_name = self.dic_ab_class[self.current_class.get_class()]["Name"]
        self.seen = ["Barbarian"]
        self.current_portrayal_name_img = None

    def main(self):
        """
        call all the methods to display the creation menu's buttons, inputbox,
        texts and dictionnaries that will be necessary to the
        character's creation
        """

        pygame.init()

        pygame.display.set_caption("D&D character creation")

        xstart = self.display_width / 8
        y_pos = self.display_height / 2.5
        xend = self.display_width / 3

        offset_x = (self.display_width / 3) - (self.display_width / 8) + 275
        offset_y = 100
        offset_x_bouton = 225

        input_box = InputBox(
            self.display_width / 8 + offset_x_bouton + 100,
            (self.display_height / 4) - 15,
            140,
            32,
            self.current_name,
        )

        abilities = [
            "Strength",
            "Charisma",
            "Intelligence",
            "Wisdom",
            "Dexterity",
            "Constitution",
        ]
        list_ability_control = []
        for i, _ in enumerate(abilities):
            abilit = abilities[i]
            if i < 3:
                xpos = xstart + 150
                ypos = y_pos + offset_y * i
                off = xend - xstart
                list_ability_control.append(
                    AbilityControl(
                        xpos,
                        ypos,
                        abilit,
                        off,
                        self.current_ab.add_functions[abilit[:3]],
                        self.current_ab.sub_functions[abilit[:3]],
                    )
                )
            else:
                xpos = xstart + offset_x + 150
                ypos = y_pos + offset_y * (i % 3)
                off = xend - xstart
                list_ability_control.append(
                    AbilityControl(
                        xpos,
                        ypos,
                        abilit,
                        off,
                        self.current_ab.add_functions[abilit[:3]],
                        self.current_ab.sub_functions[abilit[:3]],
                    )
                )
        classe_control = ClassControl(
            xstart + offset_x,
            (self.display_height / 4) - 25,
            xend - xstart + 25,
            self.current_class.set_class_next,
            self.current_class.set_class_prev,
        )
        classe_control_buttons = classe_control.get_buttons()

        list_buttons = [i.get_buttons() for i in list_ability_control]
        buttons = []
        for i, _ in enumerate(list_buttons):
            for j in range(len(list_buttons[i])):
                buttons.append(list_buttons[i][j])

        for i in classe_control_buttons:
            buttons.append(i)

        reset = Button(
            "Reset",
            xend + 200,
            y_pos + (offset_y * 3),
            100,
            50,
            self.current_ab.reset_ability,
        )
        start = Button(
            "Start",
            xend + 350,
            y_pos + (offset_y * 3),
            100,
            50,
            Creation().creation_perso,
        )
        bexit = Button(
            "Exit",
            self.display_width / (self.display_width - 10) + 125,
            self.display_height / 1.1,
            100,
            50,
            self.quitgame,
        )
        buttons.append(reset)
        buttons.append(bexit)
        portrayal_img_folder = path.join(
            self.game_folder,
            "img\\" + "portrayal_bank\\" + self.current_class.get_class(),
        )
        portrayal = pygame.image.load(
            path.join(portrayal_img_folder, self.current_class.portrayal)
        )
        portrayal_resize = pygame.transform.rotozoom(portrayal, 0, 1 / 4)

        while self.active:

            mouse = pygame.mouse.get_pos()
            for i in buttons:
                i.set_status_on_mouse(mouse)
            start.set_status_on_mouse(mouse)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                input_box.handle_event(event)

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for i in buttons:
                        i.do_action()
                    self.save_before_change()
                    if (
                        all(
                            self.dic_ab_class[i]["Name"] != input_box.text_begining
                            for i in self.dic_ab_class
                        )
                        and all(
                            self.dic_ab_class[i]["Ab"]["Points"] <= 3
                            for i in self.dic_ab_class
                        )
                        and self.allseen()
                    ):
                        for i in self.dic_ab_class:
                            start.do_action(
                                self.dic_ab_class[i]["Name"],
                                i,
                                self.dic_ab_class[i]["portrayal_name_img"],
                                self.dic_ab_class[i]["Ab"]["dic_Ab"],
                                self,
                            )

            input_box.update()

            self.gamedisplay.blit(self.imgfont, (0, 0))

            self.gamedisplay.blit(portrayal_resize, (xstart - 150, y_pos - 50))

            input_box.draw(self.gamedisplay)
            self.current_name = input_box.text

            for i in list_ability_control:
                i.draw(self.gamedisplay, self.current_ab.dic_ab[i.ability[:3]])

            classe_control.draw(self.gamedisplay, self.current_class.get_class())
            reset.draw(self.gamedisplay)
            self.dic_ab_class[self.current_class.get_class()][
                "Name"
            ] = (
                self.current_name
            )  # allow to refresh the name of the current character for the test
            # this test allow to display the start button only when all the characters are created or seen
            if (
                all(
                    self.dic_ab_class[i]["Name"] != input_box.text_begining
                    for i in self.dic_ab_class
                )
                and all(
                    self.dic_ab_class[i]["Ab"]["Points"] <= 0 for i in self.dic_ab_class
                )
                and self.allseen()
            ):
                start.draw(self.gamedisplay)
            bexit.draw(self.gamedisplay)

            self.aff_text(
                "Create your character",
                80,
                (self.display_width / 2, self.display_height / 8),
                self.gamedisplay,
            )
            self.aff_text(
                "Points:" + str(self.current_ab.points),
                40,
                (self.display_width / 8, self.display_height / 4),
                self.gamedisplay,
            )
            self.aff_text(
                "Your name : ",
                40,
                (self.display_width / 8 + offset_x_bouton, self.display_height / 4),
                self.gamedisplay,
            )
            self.aff_text(
                "character number: " + str(self.current_class.class_id + 1) + "/3",
                35,
                (self.display_width - 200, self.display_height - 20),
                self.gamedisplay,
            )

            pygame.display.update()
            self.clock.tick(60)

    def quitgame(self):
        """quit/close the window"""
        pygame.quit()
        quit()

    def aff_text(self, msg, size, pos, display: pygame.Surface):
        """allow to display the message with a specific size
        on a screen according to the X and Y coordinates

        Parameters
        ----------
        msg : str
            the text which will be displayed on the screen
        size : int
            size of the text on the screen
        X, Y : float
            coordinates where the text has to be displayed
        display : Surface
            screen where the text has to be displayed
        """

        text = pygame.font.Font(
            path.join(self.font_folder, "brushscriptitalique.ttf"), size
        )
        textsurf = text.render(msg, True, Menu_colors().black)
        textrect = textsurf.get_rect()
        textrect.center = (pos[0], pos[1])
        display.blit(textsurf, textrect)

    def initialised(self, _class):
        """Allow to initialised the abilities' dictionnary"""
        abilit = Ability(_class)
        # allow to separate the pointer of the Ab associated to the class with the others
        abilit.reset_ability()
        return {"Points": abilit.points, "dic_Ab": abilit.dic_ab}

    def save_before_change(self):
        """Allow to save/stock the values associated to the current class"""
        self.dic_ab_class[self.current_class.get_class()]["Ab"][
            "Points"
        ] = self.current_ab.points
        self.dic_ab_class[self.current_class.get_class()]["Ab"][
            "dic_Ab"
        ] = self.current_ab.dic_ab
        self.dic_ab_class[self.current_class.get_class()]["Name"] = self.current_name
        portrayal = self.current_class.portrayal
        self.dic_ab_class[self.current_class.get_class()][
            "portrayal_name_img"
        ] = portrayal

    def change_current_ab(self):
        """Allow to change the current class and display the good associated values/informations"""
        self.current_ab = Ability(
            self.current_class.get_class(),
            self.dic_ab_class[self.current_class.get_class()]["Ab"]["dic_Ab"],
            self.dic_ab_class[self.current_class.get_class()]["Ab"]["Points"],
        )
        if self.current_class.get_class() not in self.seen:
            self.seen.append(self.current_class.get_class())
        self.current_name = self.dic_ab_class[self.current_class.get_class()]["Name"]
        self.main()
        # allow to associate the good abilities' values with the class (and so re-create the buttons)

    def allseen(self):
        """indicate if all the characters were seen by the user"""
        if all(i in self.seen for i in ["Wizard", "Barbarian", "Rogue"]):
            return True
        else:
            return False

    def close(self):
        """Allow to close the window/stop to display the creation menu
        when the characters/three classes are saved"""
        self.count += 1
        if self.count == 3:
            self.active = False
