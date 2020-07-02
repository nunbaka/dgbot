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

    def getName(self):
        try:
            return self['msg']['embed']['title']
        except Exception:
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

    def get_element(self, elm_name) -> (Element):
        elm_id = unidecode(str.lower(elm_name))
        if existKey(elm_id, self):
            return Element(self[elm_id])
        return None

    def add_element(self, elm_dict) -> (Element):
        try:
            elm_id = str.lower(unidecode(elm_dict['msg']['embed']['title']))
            self.update({elm_id: elm_dict})
            return Element(elm_dict)
        except Exception:
            return None

    def remove_element(self, elm_name) -> (Element):
        elm_id = unidecode(str.lower(elm_name))
        if existKey(elm_id, self):
            elm = Element(self[elm_id])
            del self[elm_id]
            return elm
        return None

    def exist_element(self, elm_name) -> (Element):
        elm_id = unidecode(str.lower(elm_name))
        return existKey(elm_id, self)