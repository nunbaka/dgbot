from library import existKey
from discord import Embed


class Context:
    def __init__(self, client, prefix, message):
        self.client = client
        self.prefix = prefix
        self.message = message
        self.guild = message.guild
        self.author = message.author
        self.channel = message.channel
        self.users = message.mentions

    def setArgs(self, args, comment):
        self.args = args
        self.comment = comment

    async def sendChannel(self, message, **kv):
        content = self.getMessage(message['content'], **kv)
        embed = self.getEmbed(message['embed'], **kv)
        reactions = message['reactions']
        ctx = await self.channel.send(content, embed=embed)
        for reaction in reactions:
            try:
                await ctx.add_reaction(reaction)
            except Exception:
                pass

    def sendAuthor(self):
        pass

    def getMessage(self, message, total="", expression=""):
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

    def getEmbed(self, embed, **kv):
        if len(list(embed.keys())) == 0:
            return None
        e = Embed(
            title=self.getMessage(embed['title'], **kv),
            description=self.getMessage(embed['description'], **kv),
            color=embed['color'])
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
