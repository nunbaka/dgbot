from library import existKey, getTimeKey, RD, IRD
from classes.Database import Database
from unidecode import unidecode
from classes.DataList import Element
from classes.Interface.ReactionMessage import PageMessage


# classe de inventario
# contém listas pre definidas de armazenamento de itens
# não contém protocolo para aceitar dados
# tem função show, função iv
# função show procura no item controller o item
# se o item não for publico ele printa se somente se tiver o item
# função iv printa o que esté no inventário

# player contém o player dono do inventário
# self.ic contém o item controller
# stack, singles
# stacks contém a referncia de itens que existe no item controller
# singles contém itens unicos

class Inventory:
    def __init__(self, player, ic):
        self.player = player
        self.ic = ic
        self.strings = player.strings['inventory']
        # dict de itens stackaveis
        self.stacks = Database(
            pathfile=player.local+"stacks.json")
        # dict de itens não stackaveis
        self.singles = Database(
            pathfile=player.local+"singles.json")
        # comandos para esta classe
        self.commands = {
            "show": self.showItem,
            "iv": self.sendInventory
        }

    def getPages(self):
        # retorna uma lista de páginas que conténdo o inventario
        stackPages = []
        i = 0
        text = "```Itens```"
        # para cada item crie uma string e adicione ao texto
        for name_id, item in self.stacks.items():
            text += f"{i} - {item['title']}, x{item['qtd']}\n"
            i += 1
            if (i+1) % 10 == 0:
                # se deu 10 elementos crie uma página
                stackPages.append(text)
                text = ""
        if len(text) > 0:
            stackPages.append(text)
        singlePages = []
        itemPages = []
        singleItems = []
        i = 1
        text = "```Itens Unicos```"
        # para cada item crie uma string e adicione ao texto
        for name_id, item in self.singles.items():
            text += f"{RD[str(i)]} - {item['msg']['embed']['title']}, id: `{name_id}`\n"
            singleItems.append(name_id)
            i += 1
            if (i-1) % 5 == 0:
                # se deu 10 elementos crie uma página
                i = 1
                singlePages.append(text)
                itemPages.append(singleItems)
                singleItems = []
                text = ""
        if len(text) > 0:
            singlePages.append(text)
        return stackPages, singlePages, itemPages

    async def sendInventory(self, context):
        stackPages, singlePages, singleItems = self.getPages()
        rm = PageMessage(context, stackPages+singlePages)
        pagesStack = len(stackPages)
        await rm.sendChannel()
        rm.reactions = ['⏪', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '⏩']
        await rm.add_reactions()
        messages = []
        commands = {'⏪': rm.previousPage, '⏩': rm.nextPage}
        while True:
            try:
                reaction, user = await rm.wait_reaction()
                emoji = reaction.emoji
                await rm.ctx.remove_reaction(emoji, user)
                if existKey(emoji, commands):
                    commands[emoji]()
                    await rm.updateMessage()
                    continue
                index = unidecode(IRD[emoji])[:-3]
                index = int(index)-1
                page = rm.page - pagesStack
                if page < 0:
                    continue
                name_id = singleItems[page][index]
                context.setArgs(name_id.split(),
                                context.comment,
                                context.club)
                for message in messages:
                    await message.delete()
                    messages.remove(message)
                    del message
                ctx = await self.showItem(context)
                messages.append(ctx)
            except Exception as inst:
                print(inst)
                return

    async def showItem(self, context):
        # inst strings
        s = self.strings
        # get title from args
        title = " ".join(context.args)
        # get id
        name_id = unidecode(str.lower(title))
        # get item dict
        item = self.ic.get(name_id)
        if not item:
            # caso item não encontrado
            if existKey(name_id, self.singles):
                # se existir em itens unicos
                item = Element(self.singles[name_id])
                return await item.send(context)
            # em caso de não existir o item
            await context.sendChannel(
                s['noItem_error'], title=title)
            return None
        if existKey(name_id, self.stacks):
            # se tem o item no inventário
            return await item.send(context)
        if item['public']:
            # se o item for publico
            return await item.send(context)
        # se o item não for publico
        return await context.sendChannel(
            s['noPublicItem'], title=title)

    def add(self, item, qtd):
        if existKey("single", item):
            # verificando se existe a tag de single
            if item['single']:
                # existe verifica se é verdadeira
                for i in range(qtd):
                    key = getTimeKey()
                    e = item['msg']['embed']
                    name_id = str.lower(unidecode(f"{e['title']}:{key}{i}"))
                    self.singles[name_id] = item
                self.singles.save()
                return True
        # caso não seja um item single, pega só a refernecia
        item = item.getRef(qtd=qtd)
        name_id = str(unidecode(item['title']))
        if existKey(name_id, self.stacks):
            self.stacks[name_id]['qtd'] += item['qtd']
            if self.stacks[name_id]['qtd'] == 0:
                del self.stacks[name_id]
        else:
            self.stacks[name_id] = item
        self.stacks.save()
        return True
