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

    def setArgs(self, args, comment):
        # setando os argumentos e o comentario do contexto
        self.args = args
        self.comment = comment

    async def sendChannel(self, message,
                          **kv) -> (discord.Message):
        try:
            # recebendo e tratando uma mensagem
            content = self.getMessage(message['content'], **kv)
            # criando o embed
            embed = None
            if existKey('embed', message):
                embed = self.getEmbed(message['embed'], **kv)
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
        except Exception:
            # error caso a mensagem esteja mal formatada
            # caso não tenha permissão para enviar mensagem no canal
            return None

    async def sendAuthor(self, message,
                         **kv):
        # o mesmo que sendChannel, porém envia para quem chamou o evento
        try:
            content = self.getMessage(message['content'], **kv)
            embed = None
            if existKey('embed', message):
                embed = self.getEmbed(message['embed'], **kv)
            ctx = await self.author.send(content, embed=embed)
            if existKey("reactions", message):
                reactions = message['reactions']
                for reaction in reactions:
                    try:
                        await ctx.add_reaction(reaction)
                    except Exception:
                        pass
        except Exception:
            # error caso a mensagem esteja mal formatada
            # caso não tenha permissão para enviar mensagem no canal
            return None

    def getMessage(self, message,
                   total="", expression=""):
        replaces = {
            ("<#author>", self.author.mention),
            ("<#total>", str(total)),
            ("<#expression>", expression),
            ("<#comment>", self.comment)
        }
        # PARA CADA DUPLA EFETUAR REPLACE
        for r, v in replaces:
            message = message.replace(r, v)
        return message

    def getEmbed(self, embed,
                 **kv) -> (discord.Embed):
        # CRIA UM EMBED, TRATANDO AS STRINGS
        if len(list(embed.keys())) == 0:
            return None
        e = discord.Embed(
            title=self.getMessage(embed['title'], **kv),
            description=self.getMessage(embed['description'], **kv),
            color=embed['color'])
        if existKey("image-url", embed):
            e.set_image(url=embed['image-url'])
        if existKey('fields', embed):
            for field in embed['fields']:
                inline = True
                if len(field) == 3:
                    inline = field[2]
                e.add_field(name=self.getMessage(field[0], **kv),
                            value=self.getMessage(field[1], **kv),
                            inline=inline)
        return e
