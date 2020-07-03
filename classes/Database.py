from context import Msg
from library import existKey, Json
from typing import Union, Tuple
from unidecode import unidecode


class Database(dict):
    def __init__(self, pathfile="", default={}, *v, **kv):
        self.pathfile = pathfile
        super().__init__(Json.loadWrite(pathfile=pathfile, default=default))

    def save(self):
        Json.write(pathfile=self.pathfile, default=self, sort_keys=True)


class Element(dict):
    def __init__(self, elm_dict={}):
        super().__init__(elm_dict)

    def get_id(self) -> Union[str, None]:
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

    def get_element(self, elm_name: str) -> Union[Element, None]:
        elm_id = self.get_id(elm_name)
        if existKey(elm_id, self):
            return self.new_element(self[elm_id])
        return None

    def add_element(self, elm_dict: dict) -> Union[Element, None]:
        try:
            elm = self.new_element(elm_dict)
            self.update({elm.get_id(): elm_dict})
            return elm
        except Exception as inst:
            print("Datalist add element error, ", inst)
            return None

    def remove_element(self, elm_name: str) -> Union[Element, None]:
        elm_id = self.get_id(elm_name)
        if existKey(elm_id, self):
            elm = self.new_element(self[elm_id])
            del self[elm_id]
            return elm
        return None


class Catalog(dict):
    def __init__(self, master, name=""):
        # o objeto genérico, apenas considera um dono
        # com um local para armazenar as informações
        self.master = master
        self.name = name
        self.datalists = Database(
            pathfile=master.local+name+"_catalog.json")
        super().__init__(self.load_datalists())

    def get_id(self, name) -> (str):
        # transofrma o nome em um id universal
        return unidecode(str.lower(name))

    def exist_datalist(self, datalist_name: str) -> (bool):
        # retorna true se existe a chave desta datalist
        # ele verifica no catalogo, porém poderia verificar na datalist
        datalist_id = self.get_id(datalist_name)
        return existKey(datalist_id, self)

    def new_datalist(self, datalist_name: str) -> (Datalist):
        # a função que cria a datalist especificamente
        # separada do codigo para que classes herdadas
        # possam alterar o tipo de datalist
        # que o catalogo armazena
        datalist_id = self.get_id(datalist_name)
        return Datalist(
            local=self.master.local+self.name+"/",
            filename=datalist_id)

    def add_datalist(self, datalist_name: str) -> (bool):
        # instancia  a datalist no catalogo
        if self.exist_datalist(datalist_name):
            # se ja existe uma datalist o nome
            return False
        # instancia
        datalist_id = self.get_id(datalist_name)
        datalist = self.new_datalist(datalist_name)
        self[datalist_id] = datalist

        # adicionando no registro
        self.datalists[datalist_id] = datalist_name
        self.datalists.save()
        return True

    def remove_datalist(self, datalist_name: str) -> (bool):
        if not self.exist_datalist(datalist_name):
            return False
        datalist_id = self.get_id(datalist_name)
        del self[datalist_id]
        del self.datalists[datalist_id]
        self.datalists.save()
        return True

    def get_datalist(self, datalist_name: str) -> (Datalist):
        datalist_id = self.get_id(datalist_name)
        return self[datalist_id]

    def add_element(self, datalist_name: str,
                    elm_dict: dict) -> (Union[Element, None]):
        try:
            if not self.exist_datalist(datalist_name):
                return None
            datalist = self.get_datalist(datalist_name)
            elm = datalist.add_element(elm_dict)
            datalist.save()
            return elm
        except Exception:
            return None

    def remove_element(self, datalist_name: str,
                       elm_name: str) -> (Union[Element, None]):
        try:
            if not self.exist_datalist(datalist_name):
                return None
            datalist = self.get_datalist(datalist_name)
            elm = datalist.remove_element(elm_name)
            datalist.save()
            return elm
        except Exception:
            return None

    def get_element(self, datalist_name: str,
                    elm_name: str) -> (Union[Element, None]):
        if not self.exist_datalist(datalist_name):
            return None
        datalist = self.get_datalist(datalist_name)
        elm = datalist.get_element(elm_name)
        return elm

    def get_element_by_name(self, elm_name: str
                            ) -> Union[Tuple[None, None], Tuple[Element, str]]:
        for datalist_id, datalist in self.items():
            elm = datalist.get_element(elm_name)
            if elm:
                return elm, datalist_id
        return None, None

    def get_pages(self) -> (list):
        pages = []
        for datalist_id, datalist in self.items():
            datalist_pages = []
            datalist_name = self.datalists[datalist_id]
            text = f"```>> {datalist_name} <<```"
            i = 0
            for elm_id, elm_dict in datalist.items():
                embed = elm_dict['msg']['embed']
                i += 1
                text += f"{i} - {embed['title']}\n"
                if i % 10 == 0:
                    datalist_pages.append(text)
                    text = ""
            if len(text) > 0:
                datalist_pages.append(text)
            pages += datalist_pages
        return pages

    def load_datalists(self) -> (dict):
        a = {}
        for datalist_id, v in self.datalists.items():
            a[datalist_id] = Datalist(
                local=self.master.local+self.name+"/", filename=datalist_id)
        return a
