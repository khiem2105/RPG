import pygame
import settings
from box import Input


def console(player, input):
    my_imput = input.split()
    command = my_imput[0]
    first_param = my_imput[1]
    second_param = my_imput[2]

    if command == "/set":
        for first_param in player.dic_player():
            if second_param.isdigit():
                player.dic_player[first_param] += second_param
            else:
                player.game.log.add_log["Invalid parameter for set please retry"]

    if command == "/heal":
        player.healh = player.dic_player["hp"] = player.dic_player["Con"] * 10
        player.mana = player.dic_player["Int"] * 10
        player.game.log.add_log["You healed yourself"]

    if command == "/give" and first_param == "item":
        if second_param.isdigit():
            player.inventory.add_item()  # TODO pas sur de savoir comment faire
        else:
            player.game.log.add_log["Invalid parameter for give item please retry"]
