''
import discord
import asyncio
from library import existKey

# author = quem enviou a mensagem
# client = o bot com as informações dele
# prefix = o prefixo da guild do contexto
# guild = a guild do contexto
# channel = o canal onde o contexto foi criado
# users = os alvos da mensagem

# -> type, indica o tipo de retorno da mensagem
# parameter: type, indica o tipo de parametro recebido


class Context:
    def __init__(self, client, prefix, message: discord.Message):
        # CRIANDO UM CONTEXTO GERAL
        self.client = client
        self.prefix = prefix
        self.message = message
        self.guild = message.guild
        self.author = message.author
        self.channel = message.channel
        self.users = message.mentions

    def setPlayer(self, player):
        self.player = player

    def setArgs(self, args, comment, club):
        # setando os argumentos e o comentario do contexto
        self.args = args
        self.comment = comment
        self.club = club

    async def sendChannel(self, message,
                          **kv) -> (discord.Message):
        try:
            msg = Msg(self, message)
            content = msg.getContent(**kv)
            embed = msg.getEmbed(**kv)
            ctx = await self.channel.send(content, embed=embed)
            if existKey("reactions", message):
                reactions = message['reactions']
                for reaction in reactions:
                    try:
                        await ctx.add_reaction(reaction)
                    except Exception:
                        pass
            # retornando a mensagem enviada
            return ctx
        except Exception as inst:
            print(inst)
            # error caso a mensagem esteja mal formatada
            # caso não tenha permissão para enviar mensagem no canal
            return None

    async def sendAuthor(self, message,
                         **kv):
        # o mesmo que sendChannel, porém envia para quem chamou o evento
        try:
            msg = Msg(self, message)
            content = msg.getContent(**kv)
            embed = msg.getEmbed(**kv)
            ctx = await self.author.send(content, embed=embed)
            if existKey("reactions", message):
                reactions = message['reactions']
                for reaction in reactions:
                    try:
                        await ctx.add_reaction(reaction)
                    except Exception:
                        pass
            # retornando a mensagem enviada
            return ctx
        except Exception:
            # error caso a mensagem esteja mal formatada
            # caso não tenha permissão para enviar mensagem no canal
            return None


class Msg(dict):
    def __init__(self, context: Context, *v, **kv):
        self.context = context
        super().__init__(*v, **kv)

    def getEmbed(self, **kv) -> (discord.Embed):
        if not existKey("embed", self):
            return None
        embed = self['embed']
        if len(list(embed.keys())) == 0:
            return None
        e = discord.Embed()
        if existKey('title', embed):
            e.title = self.handleMessage(embed['title'], **kv)
        if existKey('description', embed):
            e.description = self.handleMessage(embed['description'], **kv)
        if existKey('color', embed):
            e.color = embed['color']
        if existKey("image_url", embed):
            if embed["image_url"]:
                e.set_image(url=embed['image_url'])
        if existKey('fields', embed):
            for field in embed['fields']:
                inline = True
                if len(field) == 3:
                    inline = field[2]
                e.add_field(name=self.handleMessage(field[0], **kv),
                            value=self.handleMessage(field[1], **kv),
                            inline=inline)
        return e

    def getContent(self, **kv):
        try:
            if existKey("content", self):
                string = self.handleMessage(self['content'], **kv)
                return string
        except Exception:
            return ""

    def handleMessage(self, string,
                      total="", expression="") -> (str):
        author = self.context.author.mention
        comment = self.context.comment
        replaces = {
            ("<#author>", author),
            ("<#total>", str(total)),
            ("<#expression>", expression),
            ("<#comment>", comment)
        }
        # PARA CADA DUPLA EFETUAR REPLACE
        for r, v in replaces:
            string = string.replace(r, v)
        return string


class ReactionMessage:
    def __init__(self, context, public=True, reactions=[]):
        self.embed = ""
        self.ctx = None
        self.content = ""
        self.public = public
        self.context = context
        self.reacts = []
        self.reactions = reactions

    def setCommands(self, commands):
        self.commands = commands
        self.reactions = list(commands.keys())

    async def add_reactions(self):
        try:
            for reaction in self.reactions:
                await self.ctx.add_reaction(reaction)
        except Exception:
            pass

    async def send(self):
        channel = self.context.channel
        self.ctx = await channel.send(self.content)
        await self.add_reactions()
        return self.ctx

    async def updateMessage(self):
        await self.ctx.edit(content=self.content)

    async def wait_reaction(self, timeout=15):
        client = self.context.client
        try:
            reaction, user = await client.wait_for(
                'reaction_add',
                timeout=timeout,
                check=self.check)
            return reaction, user
        except asyncio.TimeoutError:
            await self.ctx.clear_reactions()
            return False
        else:
            if not self.public:
                await self.ctx.remove_reaction(reaction.emoji, user)

    def check(self, reaction, user):
        if reaction.emoji in self.reactions:
            if user != self.context.client.user:
                return True
        return False


class PageMessage(ReactionMessage):
    def __init__(self, context, pages=[], title='', *v, **kv):
        self.page = 0
        self.pages = pages
        self.title = title
        self.nPages = len(pages)
        super().__init__(context, *v, *kv)
        self.setCommands({
            '⏮': self.firstPage,
            '⏪': self.previousPage,
            '⏩': self.nextPage,
            '⏭': self.lastPage
        })

    async def updateMessage(self):
        self.content = self.title + self.pages[self.page]
        await super().updateMessage()

    async def firstPage(self):
        self.page = 0
        await self.updateMessage()

    async def lastPage(self):
        self.page = self.nPages - 1
        await self.updateMessage()

    async def previousPage(self):
        self.page -= 1
        if self.page < 0:
            self.page = self.nPages-1
        await self.updateMessage()

    async def nextPage(self):
        self.page += 1
        if self.page >= self.nPages:
            self.page = 0
        await self.updateMessage()

    async def send(self):
        self.content = self.pages[0]
        self.ctx = await super().send()

    async def runReaction(self):
        while True:
            try:
                reaction, user = await self.wait_reaction()
                if user == self.context.author:
                    await self.ctx.remove_reaction(reaction.emoji, user)
                    function = self.commands[reaction.emoji]
                    if function:
                        await function()
            except Exception as inst:
                print(inst)
                return self.ctx
