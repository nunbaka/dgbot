from unidecode import unidecode
from context import Context
from classes.Database import Database
from library import existKey
from typing import Union
from json import loads


class Element(dict):
    def __init__(self, *v, **kv):
        super().__init__(*v, **kv)

    async def send(self, context: Context):
        if existKey('msg', self):
            return await context.sendChannel(self['msg'])
        return None

# local termina com barra


class DataList(Database):
    def __init__(self, local="", filename=""):
        self.local = local
        self.filename = filename
        super().__init__(pathfile=local+filename)

    def setMaxSize(self, maxSize):
        self.maxSize = maxSize

    def getSize(self):
        return len(list(self.keys()))

    async def send(self, context: Context):
        channel = context.channel
        text = f"{self.filename}"
        for key, value in self.items():
            qtd = value['qtd']
            if qtd == 0:
                qtd = ""
            else:
                qtd = f"x{qtd}"
            text += f"{value['name']}{qtd}, {value['description']}\n"
        return await channel.send(text)

    def get(self, name) -> (Union[Element, None]):
        id = unidecode(str.lower(name))
        if existKey(id, self):
            elm = self[id]
            elm = Element(
                elm['name'],
                elm['description'],
                elm['image_url'],
                elm['qtd'])
            return elm
        return None

    def add(self, _dict) -> (Element):
        if existKey('qtd', _dict):
            if existKey(_dict['id'], self):
                self[_dict['id']]['qtd'] += int(_dict['qtd'])
                return Element(_dict)
        else:
            self.update({_dict['id']: _dict})
            return Element(_dict)

    def getElement(self, _dict) -> (Element):
        e = loads(_dict)
        if existKey('name', e):
            name = e['name']
        else:
            return None
        description = ""
        if existKey("description", e):
            description = e['description']
        qtd = 0
        if existKey('qtd', e):
            qtd = e['qtd']
        image_url = ""
        if existKey('image_url', e):
            image_url = e['image_url']

        return Element(name, description, image_url=image_url, qtd=qtd)
