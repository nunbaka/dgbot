from library import existKey
import discord

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
