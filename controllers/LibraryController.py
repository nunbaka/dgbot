from classes.Database import Database
from classes.DataList import DataList
from unidecode import unidecode
from library import getCurrentTime
from json import loads


class LibraryController(dict):
    def __init__(self, club):
        self.club = club
        self.strings = club.strings.lc
        self.categories = Database(
            pathfile=club.local+"categories.json")
        self.commands = {
            "new category ": self.newCategory,
            "add": self.add
        }
        super().__init__(self.loadCategories())

    async def add(self, context):
        category = context.args[0]
        category = unidecode(str.lower(category))
        _dict = loads(context.comment)
        elm = self[category].add(_dict)
        self[category].save()
        await elm.send(context)

    async def newCategory(self, context):
        name = context.args[0]
        key = unidecode(str.lower(name))
        self[key] = DataList(
            local=self.club.local+"categories/", filename=key+".json")
        self.categories.update({key: getCurrentTime()})
        self.categories.save()
        await context.channel.send(f"Categoria {key} Criada")

    def loadCategories(self):
        a = {}
        for category, v in self.categories.items():
            a[category] = DataList(
                local=self.club.local+"categories/", filename=category+".json")
        return a
