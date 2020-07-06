from library import Json, getKey
from typing import Union, Tuple
from classes.MasterBehavior import MasterBehavior, Message, Dict, Event
from json import loads
from classes.interface.ReactionMessage import PageMessage


class Database(MasterBehavior):
    def __init__(self, master, key, tKey=""):
        super().__init__(master, key)
        self.key += tKey
        self.dict__init__(Json.loadWrite(self.local+self.key))

    def save(self):
        Json.write(pathfile=self.local+self.key, default=self, sort_keys=True)


class Element(Dict):
    def __init__(self, elm_dict={}):
        super().__init__(elm_dict)
        self.key = getKey(self['name'])

    def __str__(self):
        return self['name']

    def getEmbed(self) -> (dict):
        embed = {
            'title': self['name'],
            'description': self['description'],
            'image': self['image'],
            'footer': self['tags']
        }
        return embed

    def getMessage(self):
        message = {
            'content': "",
            'embed': self.getEmbed()
        }
        return Message(message)

    def isPublic(self) -> bool:
        return self['public']


class Datalist(Database):
    def __init__(self, master, key, tkey="_datalist"):
        super().__init__(master, key, tkey)

    def new_element(self, elm_dict: dict) -> Element:
        # a função que cria a datalist especificamente
        # separada do codigo para que classes herdadas
        # possam alterar o tipo de datalist
        # que o catalogo armazena
        return Element(elm_dict)

    def add_element(self, elm_dict: dict) -> Element:
        elm = self.new_element(elm_dict)
        self.update({elm.key: elm_dict})
        return elm

    def remove_element(self, elm_name: str) -> Element:
        elm_dict = self.delete(elm_name)
        elm = self.new_element(elm_dict)
        return elm

    def get_element(self, elm_name: str) -> Element:
        return self.new_element(self[elm_name])

    def get_pages(self, limit=10):
        values = list(self.values())
        pages = []
        text = ""
        for i in range(len(values)):
            elm = self.new_element(values[i])
            if elm.isPublic():
                i += 1
                text += f"\t{i}: {elm}\n"
                if i % limit == 0:
                    pages.append(text)
                    text = ""
        if len(text) > 0:
            pages.append(text)
            text = ""
        return pages


class Catalog(MasterBehavior):
    def __init__(self, master, key):
        super().__init__(master, key)
        self.local += self.key+"/"
        self.datalists = Database(self, key, tKey="_catalog")
        self.dict__init__(self.load_datalists())

    def new_datalist(self, datalist_name: str) -> (Datalist):
        # a função que cria a datalist especificamente
        # separada do codigo para que classes herdadas
        # possam alterar o tipo de datalist
        # que o catalogo armazena
        return Datalist(self, datalist_name)

    def add_datalist(self, datalist_name: str) -> (bool):
        # instancia  a datalist no catalogo
        if self.contain(datalist_name):
            # se ja existe uma datalist o nome
            return False
        # instancia
        datalist = self.new_datalist(datalist_name)
        self[datalist_name] = datalist
        # adicionando no registro
        self.datalists[datalist_name] = datalist_name
        self.datalists.save()
        return True

    def remove_datalist(self, datalist_name: str) -> (Datalist):
        datalist: Datalist = self.delete(datalist_name)
        if self.datalists.delete(datalist_name):
            self.datalists.save()
        return datalist

    def add_element(self, datalist_name: str,
                    elm_dict: Dict) -> (Union[Element, None]):
        try:
            datalist: Datalist = self[datalist_name]
            elm = datalist.add_element(elm_dict)
            datalist.save()
            return elm
        except Exception:
            return None

    def remove_element(self, datalist_name: str,
                       elm_name: str) -> (Union[Element, None]):
        try:
            datalist: Datalist = self[datalist_name]
            elm: Element = datalist.delete(elm_name)
            datalist.save()
            return elm
        except Exception:
            return None

    def get_element(self, datalist_name: str,
                    elm_name: str) -> (Union[Element, None]):
        try:
            datalist: Datalist = self[datalist_name]
            elm: Element = datalist.get_element(elm_name)
            return elm
        except Exception:
            return None

    def get_element_by_name(self, elm_name: str
                            ) -> Union[Tuple[None, None], Tuple[Element, str]]:
        for datalist_key, datalist in self.items():
            if not datalist:
                continue
            elm = datalist.get_element(elm_name)
            if elm:
                return elm, datalist_key
        return None, None

    def get_all_pages(self) -> (list):
        pages = []
        for datalist_key, datalist in self.items():
            if not datalist:
                continue
            datalist_page = datalist.get_pages()
            datalist_name = self.datalists[datalist_key]
            datalist_title = f"```>>> {datalist_name} <<<```"
            datalist_page[0] = datalist_title+datalist_page[0]
            pages += datalist_page
        return pages

    def load_datalists(self) -> (dict):
        a = {}
        for datalist_key, datalist_info in self.datalists.items():
            a[datalist_key] = self.new_datalist(datalist_key)
        return a


class Library(Catalog):
    def __init__(self, master, key):
        super().__init__(master, key)

    async def add_datalist(self, event):
        # cria uma nova datalist
        s = self.strings['add_datalist']
        # recebe o nome da datalist
        datalist_name = " ".join(event.args)
        success = super().add_datalist(datalist_name)
        if success:
            return await event.send(
                s['success'],
                title=datalist_name)
        await event.send(
            s['already_exist'],
            title=datalist_name
        )
        return None

    async def remove_datalist(self, event):
        # cria uma nova datalist
        s = self.strings['remove_datalist']
        # cria uma nova datalist
        datalist_name = " ".join(event.args)
        success = super().remove_datalist(datalist_name)
        if success:
            # em caso de sucesso
            return await event.send(
                s['success'],
                title=datalist_name)
        # não existir datalist
        await event.send(
            s['no_datalist_fail'],
            title=datalist_name)
        return None

    async def add_element(self, event):
        # adiciona um elemento a uma datalist presente no catalogo
        s = self.strings['add_element']
        # pegando o nome da datalist
        datalist_name = " ".join(event.args)
        if len(datalist_name) == 0:
            await event.send(
                s['datalist_no_arg'])
            return None
        try:
            # pegando o dicionário do elemento
            elm_dict = loads(event.comment)
        except Exception:
            # em caso de dicionário mal informado
            await event.send(
                s['dict_error'])
            return None
        # tentando adicionar a datalist
        elm = super().add_element(datalist_name, elm_dict)
        if elm:
            # em caso de sucesso
            elm_msg = elm.getMessage()
            elm_success = Message(s['success'])
            elm_msg.mergeMessage(elm_success)
            return await event.send(elm_msg)
        # em caso de falha (sem datalist)
        await event.send(
            s['no_datalist_error'],
            title=datalist_name)
        return None

    async def remove_element(self, event):
        # remove um elemento de uma datalist do catalogo
        s = self.strings['remove_element']
        try:
            # pega o primeiro argumento como nome do catalogo
            datalist_name = event.args[0]
            # pega o resto dos argumentos como nome do elemento
            elm_name = " ".join(event.args[1:])
        except Exception:
            # em caso de uma entrada mal informada
            await event.send(
                s['args_error'])
        # tentativa de remover o elemento da datalist
        elm = super().remove_element(datalist_name, elm_name)
        if elm:
            # dando merge na mensagem do player + a de sucesso
            msg = elm.getMsg()
            msg.mergeMessage(s['success'])
            return await event.send(
                msg, title=elm_name)
        # em caso de falha:
        # pode ser por não existir datalist
        # ou por não existir o elemento
        await event.sendChannel(
            s['no_exist_fail'])
        return None

    async def show_element(self, event: Event):
        # mostrar o elemento de uma categoria
        datalist_name = event.args[0]
        datalist: Datalist = self[datalist_name]
        if not datalist:
            print("no datalist")
            return None
        elm_name = " ".join(event.args[1:])
        elm = datalist.get_element(elm_name)
        if not elm:
            print("No Elm")
            return None
        elm_message = elm.getMessage()
        return await event.send(elm_message)

    async def show_element_by_name(self, event):
        # mostrar o elemento de uma categoria
        elm_name = " ".join(event.args)
        elm, _ = self.get_element_by_name(elm_name)
        if not elm:
            print("No Elm")
            return None
        elm_message = elm.getMessage()
        return await event.send(elm_message)
        pass

    async def show_datalist(self, event):
        # mostrar o elemento de uma categoria
        datalist_name = " ".join(event.args)
        datalist: Datalist = self[datalist_name]
        if not datalist:
            print("no datalist")
            return False
        datalist_name = self.datalists[datalist_name]
        datalist_title = f"```>>> {datalist_name} <<<```"
        datalist_pages = datalist.get_pages()
        pm = PageMessage(
            event,
            datalist_pages,
            title=datalist_title)
        await pm.run()
        return True

    async def show_catalog(self, event):
        catalog_pages = self.get_all_pages()
        pm = PageMessage(
            event,
            catalog_pages,
            title=self.strings["catalog_name"])
        await pm.run()
        return True
