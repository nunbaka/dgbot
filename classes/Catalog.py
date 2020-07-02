from unidecode import unidecode
from classes.Database import Database
from json import loads
from classes.DataList import DataList, Element
from classes.Interface.ReactionMessage import PageMessage
from library import getCurrentTime, existKey
from typing import Union

class Catalog(dict):
    def __init__(self, club, name=""):
        self.club = club
        self.name = name
        self.datalists = Database(
            pathfile=club.local+name+"_datalists.json")
        super().__init__(self.load_datalists())

    def add_element(self, datalist_name: str, elm_dict: dict) -> (Element):
        datalist_id = unidecode(str.lower(datalist_name))
        if existKey(datalist_id, self):
            elm = self[datalist_id].add(elm_dict)
            self[datalist_id].save()
            return elm
        return None

    def remove_element(self, datalist_name: str, elm_name: str) -> (Element):
        datalist_id = unidecode(str.lower(datalist_name))
        elm_id = unidecode(str.lower(elm_name))
        if existKey(datalist_id, self):
            if existKey(elm_id, self[datalist_id]):
                elm = Element(self[datalist_id][elm_id])
                del self[datalist_id][elm_id]
                self[datalist_id].save()
                return elm
        return None
        
    def new_datalist(self, datalist_name: str) -> (DataList):
        datalist_id = unidecode(str.lower(datalist_name))
        self[datalist_id] = DataList(
            local=self.club.local+f"datalists/{self.name}/", filename=datalist_id)
        self.datalists[datalist_id] = getCurrentTime()
        self.datalists.save()
        return self[datalist_id]

    def del_datalist(self, datalist_name: str) -> (DataList):
        datalist_id = unidecode(str.lower(datalist_name))
        if existKey(datalist_id, self):
            datalist = self[datalist_id]
            del self[datalist_id]
            del self.datalists[datalist_id]
            self.datalists.save()
            return datalist
        return None

    def get_element(self, elm_name) -> (Element):
        elm_id = unidecode(str.lower(elm_name))
        for datalist in list(self.keys()):
            elm = self[datalist].get(elm_name)
            if elm:
                return elm
        return None

    def get_pages(self):
        pages = []
        for datalist_id, datalist in self.items():
            datalist_pages = []
            text = f"```>> {datalist_id.capitalize()} <<```" 
            i = 0
            for elm_id, elm_dict in datalist.items():
                embed = elm_dict['msg']['embed']
                i += 1
                text += f"{i} - {embed['title']}\n"
                if i%10==0:
                    datalist_pages.append(text)
                    text = ""
            if len(text)>0:
                datalist_pages.append(text)
            pages += datalist_pages
        return pages
    
    def load_datalists(self):
        a = {}
        for datalist_id, v in self.datalists.items():
            a[datalist_id] = DataList(
                local=self.club.local+"datalists/", filename=datalist_id)
        return a

class CatalogAsync(Catalog):
    def __init__(self, *v, **kv):
        super().__init__(*v, **kv)

    async def add_element(self, context):
        # pegando o nome da datalist
        datalist_name = " ".join(context.args)
        try:
            # pegando o dicionário do elemento
            elm_dict = loads(context.comment)
        except Exception:
            # em caso de dicionário mal informado
            await context.sendChannel(
                self.strings['add_element:dict_error'])
            return None
        # tentando adicionar a datalist
        elm = super().add_element(datalist_name, elm_dict)
        if elm:
            # em caso de sucesso
            await context.sendChannel(
                self.strings['add_element:success'])
            return await elm.send(context)
        # em caso de falha (sem datalist)
        await context.sendChannel(
            self.strings['add_element:no_datalist_error'],
            title = datalist_name)
        return None

    async def remove_element(self, context):
        try:
            datalist_name = args[0]
            elm_name = args[1]
        except Exception:
            await context.sendChannel(
                self.strings['remove_element:args_error'])
        elm = super().remove_element(datalist_name, elm_name)
        if elm:
            return await elm.send(context)
        await context.sendChannel(self.strings['remove_element_error'])
        return None

    async def new_datalist(self, context):
        s = self.strings
        datalist_name = " ".join(context.args)
        datalist = super().new_datalist(datalist_name)
        if datalist:
            return await context.sendChannel(s['new_datalist_success'],
                                             title=datalist_name)

    async def del_datalist(self, context):
        s = self.strings
        datalist_name = " ".join(context.args)
        datalist = super().del_datalist(datalist_name)
        if datalist:
            return await context.sendChannel(s['del_datalist_success'],
                                             title=datalist_name)
        return
    async def send_catalog(self, context):
        pages = self.get_pages()
        rm = PageMessage(context,
                         pages,
                         self.strings['catalog_name'])
        await rm.sendChannel()
        await rm.add_reactions()
        await rm.run()