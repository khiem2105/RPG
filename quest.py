from os import path
import csv


class Quest:
    def __init__(self):
        game_folder = path.dirname(__file__)
        data_quest = path.join(game_folder, "data/quest.csv")
        file_quest = open(data_quest)
        reader = csv.reader(file_quest, delimiter=";")
        next(reader)
        self.quest_list = {}
        for raw in reader:
            self.quest_list[raw[0]] = {}
            self.quest_list[raw[0]]["name"] = raw[1]
            self.quest_list[raw[0]]["type"] = raw[2]
            self.quest_list[raw[0]]["objective"] = raw[3]
            if raw[2] == "1":
                self.quest_list[raw[0]]["enemy"] = raw[4]
            elif raw[2] == "0":
                self.quest_list[raw[0]]["item"] = raw[5]
            elif raw[2] == "2":
                self.quest_list[raw[0]]["enemy"] = raw[4]
                self.quest_list[raw[0]]["item"] = raw[5]
            elif raw[2] == "3":
                self.quest_list[raw[0]]["enemy"] = raw[4]
                self.quest_list[raw[0]]["item"] = []
                for item in raw[5].split(","):
                    self.quest_list[raw[0]]["item"].append(item)
            self.quest_list[raw[0]]["type_reward"] = raw[6]
            self.quest_list[raw[0]]["reward"] = raw[7]
