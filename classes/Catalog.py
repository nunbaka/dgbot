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

    def add_element(self, datalist_name: str, elm_dict: dict) -> (Union[Element, None]):
        datalist_id = unidecode(str.lower(datalist_name))
        if existKey(datalist_id, self):
            elm = self[datalist_id].add(elm_dict)
            self[datalist_id].save()
            return elm
        return None

    def remove_element(self, datalist_name: str, elm_name: str) -> (Union[Element, None]):
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

    def get_element(self, elm_name) -> (Union[Element, None]):
        elm_id = unidecode(str.lower(elm_name))
        for datalist in list(self.keys()):
            elm = self[datalist].get(elm_name)
            if elm:
                return elm
        return None

    def load_datalists(self):
        a = {}
        for datalist_id, v in self.datalists.items():
            a[datalist_id] = DataList(
                local=self.club.local+"datalists/", filename=datalist_id)
        return a

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
    
class CatalogAsync(Catalog):
    def __init__(self, *v, **kv):
        super().__init__(*v, **kv)

    async def add_element(self, context):
        datalist_name = " ".join(context.args)
        try:
            elm_dict = loads(context.comment)
        except:
            print("Dicionário Inválido")
            return None
        elm = super().add_element(datalist_name, elm_dict)
        if elm:
            return await elm.send(context)
        await context.sendChannel(self.strings['noDatalist_error'])
        return None

    async def remove_element(self, context):
        args = context.args
        try:
            datalist_name = args[0]
            elm_name = args[1]
        except Exception:
            # arg error
            await context.sendChannel(self.strings['remove_element_args_error'])
        elm = super().remove_element(datalist_name, elm_name)
        if elm:
            return await elm.send(context)
        await context.sendChannel(self.strings['remove_element_error'])
        return None

    async def new_dataList(self, context):
        s = self.strings
        datalist_name = " ".join(context.args)
        datalist = super().new_datalist(datalist_name)
        return await context.sendChannel(s['created_datalist'],
                                         title=datalist_name)

    async def send_catalog(self, context):
        pages = self.get_pages()
        rm = PageMessage(context,
                         pages,
                         self.strings['catalog_name'])
        await rm.sendChannel()
        await rm.add_reactions()
        await rm.run()