import discord
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
        self.args = []
        self.comment = ""
        self.club = None
        self.player = None

    async def sendChannel(self, message,
                          **kv) -> (discord.Message):
        try:
            msg = Msg(message)
            content = msg.getContent(context=self, **kv)
            embed = msg.getEmbed(context=self, **kv)
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
            msg = Msg(message)
            content = msg.getContent(context=self, **kv)
            embed = msg.getEmbed(context=self, **kv)
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
    def __init__(self, *v, **kv):
        super().__init__(*v, **kv)

    def mergeMessage(self, message):
        try:
            if not existKey('content', self):
                self['content'] = message['content']
            else:
                self['content'] = self['content']+"\n\n"+message['content']
        except Exception:
            pass
        try:
            if not existKey('embed', self):
                self['embed'] = message['embed']
            else:
                d = self['embed']['description']
                d2 = message['embed']['description']
                self['embed']['description'] = d+'\n\n'+d2
        except Exception:
            pass
        return self

    def setContent(self, content):
        try:
            self['content'] = content
        except Exception:
            pass

    def setDescription(self, description):
        try:
            self['embed']['description'] = description
        except Exception:
            pass

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
            return self.handleMessage(self['content'], **kv)
        except Exception:
            return ""

    def handleMessage(
            self, string, context=None,
            total="",
            expression="",
            title="",
            user="",
            qtd=0) -> (str):
        author = context.author.mention
        comment = context.comment
        replaces = {
            ("<#author>", author),
            ("<#total>", str(total)),
            ("<#expression>", expression),
            ("<#comment>", comment),
            ("<#title>", title),
            ("<#user>", user),
            ("<#qtd>", str(qtd))

        }
        # PARA CADA DUPLA EFETUAR REPLACE
        for r, v in replaces:
            string = string.replace(r, v)
        return string
