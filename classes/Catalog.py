from unidecode import unidecode
from classes.Database import Database
from json import loads
from classes.DataList import DataList, Element
from classes.Interface.ReactionMessage import PageMessage
from library import getCurrentTime, existKey
from typing import Union

# uma datalist é como se fosse uma categoria
# um elemento é um dado que aquela categoria dada
# um catalaogo contém várias categorias

class Catalog(dict):
    def __init__(self, master, name=""):
        self.master = master
        self.name = name
        self.datalists = Database(
            pathfile=master.local+name+"_catalog.json")
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
            local=self.master.local+f"datalists/{self.name}/", filename=datalist_id)
        self.datalists[datalist_id] = datalist_name
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

    def get_element(self, datalist_name: str, elm_name: str) -> (Element):
        elm_id = unidecode(str.lower(elm_name))
        datalist_id = unidecode(str.lower(datalist_name))
        if existKey(datalist_id, self):
            if existKey(elm_id, self[datalist_id]):
                return Element(self[datalist_id][elm_id])
            # erro que não existe o elemento id
            print("Not Exist Element ID in get_element")
        # erro que não existe a datalist id
        print("not Exist datalist_id in get element")
        return None

    def get_element_by_name(self, elm_name:str) -> (Element):
        for datalist_id, datalist in self.items():
            elm = self.get_element(datalist_id, elm_name)
            if elm:
                return elm, datalist_id
        return None

    def get_pages(self):
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
                local=self.master.local+"datalists/", filename=datalist_id)
        return a

class Library(Catalog):
    def __init__(self, *v, **kv):
        super().__init__(*v, **kv)

    async def add_element(self, context):
        # adiciona um elemento a uma datalist presente no catalogo
        s = self.strings['add_element']
        # pegando o nome da datalist
        datalist_name = " ".join(context.args)
        try:
            # pegando o dicionário do elemento
            elm_dict = loads(context.comment)
        except Exception:
            # em caso de dicionário mal informado
            await context.sendChannel(
                s['dict_error'])
            return None
        # tentando adicionar a datalist
        elm = super().add_element(datalist_name, elm_dict)
        if elm:
            # em caso de sucesso
            await context.sendChannel(
                s['success'])
            return await elm.send(context)
        # em caso de falha (sem datalist)
        await context.sendChannel(
            s['no_datalist_error'],
            title = datalist_name)
        return None

    async def remove_element(self, context):
        # remove um elemento de uma datalist do catalogo
        s = self.strings['remove_element']
        try:
            # pega o primeiro argumento como nome do catalogo
            datalist_name = context.args[0]
            # pega o resto dos argumentos como nome do elemento
            elm_name = " ".join(context.args[1:])
        except Exception:
            # em caso de uma entrada mal informada
            await context.sendChannel(
                s['args_error'])
        # tentativa de remover o elemento da datalist
        elm = super().remove_element(datalist_name, elm_name)
        if elm:
            # em caso de sucesso, enviar mensagem de sucesso
            await context.sendChannel(
                s['success'],
                title = elm_name)
            # enviar também o elemento removido
            return await elm.send(context)
        # em caso de falha:
        # pode ser por não existir datalist
        # ou por não existir o elemento
        await context.sendChannel(
            s['no_exist_fail'])
        return None

    async def new_datalist(self, context):
        # cria uma nova datalist
        s = self.strings['new_datalist']
        # recebe o nome da datalist
        datalist_name = " ".join(context.args)
        datalist = super().new_datalist(datalist_name)
        if datalist:
            # em caso de sucesso
            return await context.sendChannel(
                s['success'],
                title=datalist_name)

    async def del_datalist(self, context):
        # cria uma nova datalist
        s = self.strings['del_datalist']
        # cria uma nova datalist
        datalist_name = " ".join(context.args)
        datalist = super().del_datalist(datalist_name)
        if datalist:
            # em caso de sucesso
            return await context.sendChannel(
                s['success'],
                title=datalist_name)
        # não existir datalist
        context.sendChannel(
            s['no_datalist_fail'],
            title= datalist_name)
        return None

    async def send_catalog(self, context):
        pages = self.get_pages()
        rm = PageMessage(context,
                         pages,
                         self.strings['catalog_name'])
        await rm.sendChannel()
        await rm.add_reactions()
        await rm.run()
