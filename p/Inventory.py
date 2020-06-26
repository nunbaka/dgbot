from library import existKey, getTimeKey
from classes.Database import Database
from unidecode import unidecode
from classes.DataList import Element


class Inventory(dict):
    def __init__(self, player, ic):
        super().__init__()
        self.player = player
        self.ic = ic
        self["stacks"] = Database(
            pathfile=player.local+"stacks.json")
        self["singles"] = Database(
            pathfile=player.local+"singles.json")
        self.commands = {
            "show": self.showItem,
            "iv": self.sendInventory
        }

    async def sendInventory(self, context):
        text = "```Items```"
        for name_id, item in self['stacks'].items():
            text += f"{item['title']} x{item['qtd']}\n"
        text += "\n```Items Únicos```"
        for name_id, item in self['singles'].items():
            e = item['msg']['embed']
            text += f"{e['title']}, id: {name_id}\n"
        await context.channel.send(text)

    async def showItem(self, context):
        name_id = " ".join(context.args)
        name_id = unidecode(str.lower(name_id))
        a = self.ic.get(name_id)
        if not a:
            if existKey(name_id, self['singles']):
                item = Element(self['singles'][name_id])
                return await item.send(context)
            await context.channel.send("No Exist")
            return None
        if existKey(name_id, self['stacks']):
            return await a.send(context)
        if a['public']:
            return await a.send(context)
        return await context.channel.send("No Public")

    def add(self, item, qtd):
        if existKey("single", item):
            if item['single']:
                key = getTimeKey()
                e = item['msg']['embed']
                name_id = str.lower(unidecode(f"{e['title']}:{key}"))
                self['singles'][name_id] = item
                self['singles'].save()
                return True
        item = item.getRef(qtd=qtd)
        name_id = str(unidecode(item['title']))
        if existKey(name_id, self['stacks']):
            self['stacks'][name_id]['qtd'] += item['qtd']
            if self['stacks'][name_id]['qtd'] == 0:
                del self['stacks'][name_id]
        else:
            self['stacks'][name_id] = item
        self['stacks'].save()
