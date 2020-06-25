from unidecode import unidecode
from context import Context
from classes.Database import Database
from library import existKey
from typing import Union
from json import loads


class Element(dict):
    def __init__(self, name, description, image_url="", qtd=0):
        super().__init__()
        self['id'] = unidecode(str.lower(name))
        self['name'] = name
        self['description'] = description
        self['image_url'] = image_url
        self['qtd'] = qtd
        self['msg'] = {
            "embed": {
                "title": self['name'],
                "description": self['description'],
                "image_url": self['image_url']
            }
        }

    async def send(self, context: Context):
        return await context.sendChannel(self['msg'])

# local termina com barra


class DataList(Database):
    def __init__(self, local="", filename="", maxSize=-1):
        self.local = local
        self.filename = filename
        self.maxSize = maxSize
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

    def add(self, element: Element) -> (Union[Element, None]):
        if existKey(element['id'], self):
            if self.maxSize != -1:
                if self[element['id']]['qtd'] + element['qtd'] > self.maxSize:
                    return None
            self[element['id']]['qtd'] = int(
                self[element['id']]['qtd'])+int(element['qtd'])

            return element
        else:
            if self.maxSize != -1:
                if element['qtd'] > self.maxSize:
                    return None
            self.update({element['id']: element})
            return element

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
