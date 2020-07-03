from unidecode import unidecode
from context import Context, Msg
from classes.Database import Database
from library import existKey
from json import loads

class Element(dict):
    def __init__(self, elm_dict={}):
        super().__init__(elm_dict)

    def get_id(self) -> (str):
        try:
            elm_name = self['msg']['embed']['title']
            elm_id = unidecode(str.lower(elm_name))
            return elm_id
        except Exception:
            return None

    def isSingle(self) -> (bool):
        if existKey('single', self):
            return self['single']
        return True
    
    def isPublic(self) -> (bool):
        if existKey('public', self):
            return self['public']
        return True

    def isUnknown(self) -> (bool):
        if existKey('unknown', self):
            return self['unknown']
        return False

    def getMsg(self) -> (Msg):
        msg = Msg(self['msg'])
        if self.isUnknown():
            msg.setDescription("")
        return msg

class Datalist(Database):
    def __init__(self, local="", filename=""):
        self.local = local
        self.filename = filename
        super().__init__(pathfile=local+filename+".json")

    def get_id(self, name) -> (str):
        return unidecode(str.lower(name))

    def exist_element(self, elm_name: str) -> (bool):
        elm_id = self.get_id(elm_name)
        return existKey(elm_id, self)

    def new_element(self, elm_dict: dict) -> (Element):
        # a função que cria a datalist especificamente
        # separada do codigo para que classes herdadas
        # possam alterar o tipo de datalist
        # que o catalogo armazena
        return Element(elm_dict)
   
    def get_element(self, elm_name: str) -> (Element):
        elm_id = self.get_id(elm_name)
        if existKey(elm_id, self):
            return self.new_element(self[elm_id])
        return None

    def add_element(self, elm_dict: dict) -> (Element):
        try:
            elm = self.new_element(elm_dict)
            self.update({elm.get_id(): elm_dict})
            return elm
        except Exception as inst:
            print("Datalist add element error, ", inst)
            return None

    def remove_element(self, elm_name: str) -> (Element):
        elm_id = self.get_id(elm_name)
        if existKey(elm_id, self):
            elm = self.new_element(self[elm_id])
            del self[elm_id]
            return elm
        return None
