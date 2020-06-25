from classes.DataList import DataList
from unidecode import unidecode


class Inventory(dict):
    def __init__(self, player):
        super().__init__()
        self.player = player
        self['weapons'] = DataList(player.local, filename="weapons.json")
        self.commands = {
            "add": self.add,
            "show": self.show
        }

    async def add(self, context):
        category = context.args[0]
        args = context.args[1:]
        elm = self[category].add(self[category].getElement(context.comment))
        if elm:
            await elm.send(context)
            self[category].save()
            return elm
        return None

    async def show(self, context):
        category = context.args[0]
        name = str.lower(unidecode(context.args[1]))
        elm = self[category].get(name)
        if elm:
            await elm.send(context)
            return elm
        return None
