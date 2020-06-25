from unidecode import unidecode
from context import Context
from classes.Database import Database
from library import existKey
from typing import Union


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
    def __init__(self, local="", filename=""):
        self.local = local
        self.filename = filename
        super().__init__(pathfile=local+filename)

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
            return self[id]
        return None

    def add(self, element: Element) -> (Element):
        if existKey(element['id'], self):
            self[element['id']]['qtd'] += element['qtd']
            return element
        else:
            self.update({element['id']: element})
            return element
