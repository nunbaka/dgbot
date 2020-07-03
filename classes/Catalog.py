from unidecode import unidecode
from classes.Database import Database
from context import Msg
from json import loads
from classes.Datalist import Datalist, Element
from classes.interface.ReactionMessage import PageMessage
from library import getCurrentTime, existKey
from typing import Tuple

# uma datalist é como se fosse uma categoria
# um elemento é um dado que aquela categoria dada
# um catalaogo contém várias categorias

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
        return Datalist(local=self.master.local+self.name+"/", filename=datalist_id)

    def add_datalist(self, datalist_name: str) -> (Datalist):
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

    def remove_datalist(self, datalist_name: str) -> (Datalist):
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

    def add_element(self, datalist_name: str, elm_dict: dict) -> (Element):
        try:
            if not self.exist_datalist(datalist_name):
                return True
            datalist = self.get_datalist(datalist_name)
            elm = datalist.add_element(elm_dict)
            datalist.save()
            return elm
        except Exception:
            return None

    def remove_element(self, datalist_name: str, elm_name: str) -> (Element):
        try:
            if not self.exist_datalist(datalist_name):
                return False
            datalist = self.get_datalist(datalist_name)
            elm = datalist.remove_element(elm_name)
            datalist.save()
            return elm
        except Exception:
            return None

    def get_element(self, datalist_name: str, elm_name: str) -> (Element):
        if not self.exist_datalist(datalist_name):
            return False
        datalist = self.get_datalist(datalist_name)
        elm = datalist.get_element(elm_name)
        return elm

    def get_element_by_name(self, elm_name:str) -> (Tuple[Element, str]):
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
                if i%10==0:
                    datalist_pages.append(text)
                    text = ""
            if len(text)>0:
                datalist_pages.append(text)
            pages += datalist_pages
        return pages
    
    def load_datalists(self) -> (dict):
        a = {}
        for datalist_id, v in self.datalists.items():
            a[datalist_id] = Datalist(
            local=self.master.local+self.name+"/", filename=datalist_id)
        return a

class Library(Catalog):
    def __init__(self, *v, **kv):
        super().__init__(*v, **kv)

    async def add_datalist(self, context):
        # cria uma nova datalist
        s = self.strings['add_datalist']
        # recebe o nome da datalist
        datalist_name = " ".join(context.args)
        success = super().add_datalist(datalist_name)
        if success:
            return await context.sendChannel(
                s['success'],
                title=datalist_name)
        await context.sendChannel(
            s['already_exist'],
            title = datalist_name
        )
        return None

    async def remove_datalist(self, context):
        # cria uma nova datalist
        s = self.strings['remove_datalist']
        # cria uma nova datalist
        datalist_name = " ".join(context.args)
        success = super().remove_datalist(datalist_name)
        if success:
            # em caso de sucesso
            return await context.sendChannel(
                s['success'],
                title=datalist_name)
        # não existir datalist
        await context.sendChannel(
            s['no_datalist_fail'],
            title= datalist_name)
        return None

    async def add_element(self, context):
        # adiciona um elemento a uma datalist presente no catalogo
        s = self.strings['add_element']
        # pegando o nome da datalist
        datalist_name = " ".join(context.args)
        if len(datalist_name)==0:
            await context.sendChannel(
                s['datalist_no_arg'])
            return None
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
            msg = elm.getMsg()
            msg.mergeMessage(s['success'])
            return await context.sendChannel(msg)
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
            # dando merge na mensagem do player + a de sucesso
            msg = elm.getMsg()
            msg.mergeMessage(s['success'])
            return await context.sendChannel(
                msg, title = elm_name)
        # em caso de falha:
        # pode ser por não existir datalist
        # ou por não existir o elemento
        await context.sendChannel(
            s['no_exist_fail'])
        return None

    async def send_catalog(self, context):
        pages = self.get_pages()
        if len(pages)==0:
            await context.sendChannel(
                self.strings['empty_catalog'])
            return None
        rm = PageMessage(context,
                         pages,
                         self.strings['catalog_name'])
        await rm.sendChannel()
        await rm.add_reactions()
        await rm.run()
