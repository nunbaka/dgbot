from classes.player.ItemStorage import ItemStorage
from classes.player.Inventory import Inventory

class Player:
    def __init__(self, club, pKey):
        self.club = club
        self.strings = self.club.strings.p
        self.key = pKey
        self.local = f"{club.local}players/{pKey}/"
        self.inventory = Inventory(
            local=self.local, filename="inventory.json")
        # self.spells = Spell()

    def getCommands(self):
        cmds = {}
        return cmds

