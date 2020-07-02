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

    def isSingle(self):
        if existKey('single', self):
            return self['single']
        return True
    
    def isPublic(self):
        if existKey('public', self):
            return self['public']
        return True
# local termina com barra


class Datalist(Database):
    def __init__(self, local="", filename=""):
        self.local = local
        self.filename = filename
        super().__init__(pathfile=local+filename+".json")

    def getSize(self):
        return len(list(self.keys()))

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
