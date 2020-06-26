from p.Inventory import Inventory


class Player:
    def __init__(self, club, pKey):
        self.club = club
        self.key = pKey
        self.local = f"{club.local}players/{pKey}/"
        self.inventory = Inventory(self, club.ic)
        # self.spells = Spell()

    def getCommands(self):
        here = [self.inventory]
        commands = {}
        for commands in here:
            commands.update(self.inventory.commands)
        return commands
