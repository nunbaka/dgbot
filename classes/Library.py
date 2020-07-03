from json import loads
from classes.Database import Catalog
from classes.interface.ReactionMessage import PageMessage

# uma datalist é como se fosse uma categoria
# um elemento é um dado que aquela categoria dada
# um catalaogo contém várias categorias


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
            title=datalist_name
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
            title=datalist_name)
        return None

    async def add_element(self, context):
        # adiciona um elemento a uma datalist presente no catalogo
        s = self.strings['add_element']
        # pegando o nome da datalist
        datalist_name = " ".join(context.args)
        if len(datalist_name) == 0:
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
            title=datalist_name)
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
                msg, title=elm_name)
        # em caso de falha:
        # pode ser por não existir datalist
        # ou por não existir o elemento
        await context.sendChannel(
            s['no_exist_fail'])
        return None

    async def send_catalog(self, context):
        pages = self.get_pages()
        if len(pages) == 0:
            await context.sendChannel(
                self.strings['empty_catalog'])
            return None
        rm = PageMessage(context,
                         pages,
                         self.strings['catalog_name'])
        await rm.sendChannel()
        await rm.add_reactions()
        await rm.run()
