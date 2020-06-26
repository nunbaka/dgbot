from classes.Database import Database
from classes.DataList import DataList, Element
from unidecode import unidecode
from library import getCurrentTime
from json import loads


class ItemController(dict):
    def __init__(self, club):
        self.club = club
        self.strings = club.strings.lc
        self.datalists = Database(
            pathfile=club.local+"datalists.json")
        self.commands = {
            "add": self.add,
            "new datalist": self.newDatalist,
            "list": self.sendList,
            "give": self.give
        }
        super().__init__(self.loadCategories())

    def get(self, title):
        for datalist in list(self.keys()):
            return self[datalist].get(title)

    async def give(self, context):
        # pessoa, item, qtd
        name_id = context.args[1]
        try:
            qtd = int(context.args[2])
        except Exception:
            qtd = 1
        item = self.get(name_id)
        if item:
            player = context.club.getPlayer(context.users[0])
            player.inventory.add(item, qtd)

    async def sendList(self, context):
        datalist = " ".join(context.args)
        datalist = unidecode(str.lower(datalist))
        await self[datalist].send(context)

    async def add(self, context):
        datalist = " ".join(context.args)
        datalist = unidecode(str.lower(datalist))
        _dict = loads(context.comment)
        elm = self[datalist].add(_dict)
        self[datalist].save()
        await elm.send(context)

    async def newDatalist(self, context):
        name = " ".join(context.args)
        datalist = unidecode(str.lower(name))
        self[datalist] = DataList(
            local=self.club.local+"datalists/", filename=datalist)
        self.datalists[datalist] = getCurrentTime()
        self.datalists.save()
        await context.channel.send(f"Datalist {datalist} Criada")

    def loadCategories(self):
        a = {}
        for datalist, v in self.datalists.items():
            a[datalist] = DataList(
                local=self.club.local+"datalists/", filename=datalist)
        return a
