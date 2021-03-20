from game import Game
from load import Load
from save import load
from event import new
from main_menu import MainMenu
import createmenu


# create the game object
menu = MainMenu()
menu.add_widget()

while True:
    menu.update()
    player_dic = None
    print("je suis dans le run")
    # allow to display the creation menu if the user want to make a new game
    if menu.state == "New Game" and menu.save_name != "" and menu.name != None:
        print("je suis après le if")
        player_dic = createmenu.CreationMenu()
        player_dic.main()
        if all("dic" in player_dic.chara_create[i] for i in player_dic.chara_create):
            break
    elif menu.name != None or menu.isload:
        break
if player_dic:
    g = Game(menu.save_name, False, menu.name, player_dic.chara_create)
else:
    g = Game(menu.save_name, False, menu.name)
g.show_start_screen()
new(g)
if menu.isload:
    load(g, menu.save_name)
while True:
    g.run()
    g.show_go_screen()
