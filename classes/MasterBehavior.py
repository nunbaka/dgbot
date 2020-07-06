from library import existKey, getKey
import discord


class Dict(dict):
    def __init__(self, _: dict):
        super().__init__(_)

    def __getitem__(self, key):
        key = getKey(key)
        if super().__contains__(key):
            return super().__getitem__(key)
        return None

    def __setitem__(self, key, value):
        key = getKey(key)
        if isinstance(value, dict):
            value = Dict(value)
        return super().__setitem__(key, value)

    def delete(self, key):
        key = getKey(key)
        if super().__contains__(key):
            del self[key]
            return True
        return False

    def exist(self, key):
        return super().__contains__(key)


class Message(Dict):
    def __init__(self, *v, **kv):
        super().__init__(*v, **kv)

    def merge(self, message):
        content = message['content']
        embed = message['embed']
        if content:
            if self.exist('content'):
                self['content'] += '\n'+content
            else:
                self['content'] = content
        if not embed:
            return self
        if not self.exist('embed'):
            self['embed'] = embed
            return self
        if not self.exist('description'):
            self['embed']['description'] = embed['description']
        else:
            self['embed']['description'] += '\n'+embed['description']
        if not self.exist('footer'):
            self['embed']['footer'] = embed['footer']
        else:
            self['embed']['footer'] += embed['footer']
        if not self.exist('reactions'):
            self['embed']['reactions'] = embed['reactions']
        else:
            self['embed']['reactions'] += embed['reactions']

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
        try:
            embed = self['embed']
            if not embed:
                return None
            e = discord.Embed()
            if existKey('footer', embed):
                footer = ", ".join(embed['footer'])
                e.set_footer(text=footer,
                             icon_url="https://i.imgur.com/l37XqXC.png")
            if existKey('title', embed):
                e.title = self.handleMessage(embed['title'], **kv)
            if existKey('description', embed):
                e.description = self.handleMessage(embed['description'], **kv)
            if existKey('color', embed):
                e.color = self.handleMessage(embed['color'], **kv)
            if existKey('image', embed):
                try:
                    if len(embed['image']) > 0:
                        e.set_image(url=embed['image'])
                except Exception:
                    pass
            return e
        except Exception as inst:
            print(inst)
            return None

    def getContent(self, **kv):
        try:
            return self.handleMessage(self['content'], **kv)
        except Exception:
            return ""

    def handleMessage(
            self, string,
            context=None,
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


class MasterBehavior(Dict):
    def __init__(self, master, key: str):
        self.master: MasterBehavior = master
        self.key = getKey(key)
        self.local: str = master.local

    def dict__init__(self, _: dict = {}):
        super().__init__(_)


class Event:
    def __init__(self, client, prefix, event_prefix, message: discord.Message):
        # CRIANDO UM CONTEXTO GERAL
        self.client = client
        self.prefix = prefix
        self.event_prefix = event_prefix
        self.message = message
        self.guild = message.guild
        self.author = message.author
        self.channel = message.channel
        self.user = None
        self.users = message.mentions
        self.args: list = []
        self.comment = ""
        self.club = None
        self.terrain = None
        self.player = None
        self.target = None
        self.targets: list = []

    async def send(self, message: Message,
                   **kv) -> (discord.Message):
        message = Message(message)
        content = message.getContent(context=self, **kv)
        embed = message.getEmbed(context=self, **kv)
        ctx = await self.channel.send(content, embed=embed)
        reactions = message['reactions']
        if reactions:
            for reaction in reactions:
                try:
                    await ctx.add_reaction(reaction)
                except Exception:
                    pass
        # retornando a mensagem enviada
        return ctx

    async def send_author(self, message,
                          **kv):
        msg = Message(message)
        content = msg.getContent(context=self, **kv)
        embed = msg.getEmbed(context=self, **kv)
        ctx = await self.author.send(content, embed=embed)
        reactions = msg['reactions']
        if reactions:
            for reaction in reactions:
                try:
                    await ctx.add_reaction(reaction)
                except Exception:
                    pass
        # retornando a mensagem enviada
        return ctx
