from unidecode import unidecode
from context import Context
from classes.Database import Database
from library import existKey
from typing import Union
from json import loads


class Element(dict):
    def __init__(self, elm_dict={}):
        super().__init__(elm_dict)

    async def send(self, context: Context):
        msg = self['msg']
        if existKey('unknown', self):
            if self['unknown']:
                msg['embed']['description'] = "Item estranho..."
        if existKey('msg', self):
            return await context.sendChannel(msg)
        return None

    def getRef(self, qtd=1):
        return {
            "title": self['msg']['embed']['title'],
            "qtd": qtd
        }
# local termina com barra


class DataList(Database):
    def __init__(self, local="", filename=""):
        self.local = local
        self.filename = filename
        super().__init__(pathfile=local+filename+".json")

    def getSize(self):
        return len(list(self.keys()))

    async def send(self, context: Context):
        channel = context.channel
        text = f"```{self.filename.capitalize()}```"
        i = 1
        for key, value in self.items():
            # e = o dicionário usado no embed
            e = value['msg']['embed']
            if value['public']:
                text += f"\t{i} - {e['title']}\n"
                i += 1
        return await channel.send(text)

    def get(self, title) -> (Union[Element, None]):
        name_id = unidecode(str.lower(title))
        if existKey(name_id, self):
            return Element(self[name_id], self.filename)
        return None

    def set(self, _dict) -> (Element):
        name_id = str.lower(unidecode(_dict['msg']['embed']['title']))
        self[name_id] = _dict
        return Element(_dict)

    def add(self, elm_dict) -> (Element):
        elm_id = str.lower(unidecode(elm_dict['msg']['embed']['title']))
        self.update({elm_id: elm_dict})
        return Element(elm_dict)


class RefList(DataList):
    def __init__(self, datalists=[], **kv):
        self.datalists = datalists
        super().__init__(**kv)

    def get(self, title):
        for datalist in self.datalists:
            elm = datalist.get(title)
            if elm:
                return elm

    async def send(self, context: Context):
        channel = context.channel
        text = f"```{self.filename.capitalize()}```"
        i = 1
        for key, value in self.items():
            # e = o dicionário usado no embed
            e = value['msg']['embed']
            text += f"\t{i} - {e['title']}\n"
            i += 1
        return await channel.send(text)
