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