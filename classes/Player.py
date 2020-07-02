from classes.player.ItemStorage import ItemStorage

class Player:
    def __init__(self, club, pKey):
        self.club = club
        self.strings = self.club.strings.p
        self.key = pKey
        self.local = f"{club.local}players/{pKey}/"
        self.inventory = ItemStorage(self, name="inventory")
        # self.spells = Spell()

    def getCommands(self):
        cmds = {}
        return cmds

