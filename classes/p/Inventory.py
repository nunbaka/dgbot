from classes.DataList import DataList


class Inventory:
    def __init__(self, player):
        self.player = player
        self.weapons = DataList(player.local, filename="weapons.json")
