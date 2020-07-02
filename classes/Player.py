from classes. import ItemStorage


class Player:
    def __init__(self, club, pKey):
        self.club = club
        self.strings = self.club.strings.p
        self.key = pKey
        self.local = f"{club.local}players/{pKey}/"
        self.inventory = ItemStorage(self, club.ic)
        # self.spells = Spell()

    def getCommands(self):
        here = [self.inventory]
        cmds = {}
        for options in here:
            cmds.update(options.commands)
        return cmds
