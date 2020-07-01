from context import Context
import asyncio

"""
    RactionMessage
    Para enviar mensagens que capturam reações

    # rm.ctx = Mensagem Enviada
    # rm.content = Texto da mensagem

"""


class ReactionMessage:
    def __init__(self, context: Context):
        self.ctx = None
        self.content = ""
        self.context = context
        self.reactions: list = []

    async def add_reactions(self):
        if not self.ctx:
            # somente se existir mensagem
            return None
        try:
            for reaction in self.reactions:
                await self.ctx.add_reaction(reaction)
            return True
        except Exception:
            return False

    async def sendChannel(self):
        channel = self.context.channel
        self.ctx = await channel.send(self.content)
        return self.ctx

    async def updateMessage(self):
        if not self.ctx:
            return None
        return await self.ctx.edit(content=self.content)

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

    def check(self, reaction, user):
        # devolve qualquer reação feita que não seja do client
        if user != self.context.client.user:
            return True
        return False


class PageMessage(ReactionMessage):
    def __init__(self, context: Context, pages=[], title=''):
        self.page = 0
        self.pages = pages
        self.title = title
        self.nPages = len(pages)
        super().__init__(context)
        self.commands = {
            '⏮': self.firstPage,
            '⏪': self.previousPage,
            '⏩': self.nextPage,
            '⏭': self.lastPage
        }
        self.reactions = list(self.commands.keys())
        self.content = self.title + self.pages[self.page]

    async def updateMessage(self):
        self.content = self.title + self.pages[self.page]
        await super().updateMessage()

    def check(self, reaction, user):
        if user == self.context.client.user:
            return False
        if not user == self.context.author:
            return False
        if not (reaction.emoji in self.reactions):
            return False
        return True

    def firstPage(self):
        self.page = 0

    def lastPage(self):
        self.page = self.nPages - 1

    def previousPage(self):
        self.page -= 1
        if self.page < 0:
            self.page = self.nPages-1

    def nextPage(self):
        self.page += 1
        if self.page >= self.nPages:
            self.page = 0

    async def run(self):
        while True:
            try:
                reaction, user = await self.wait_reaction()
                await self.ctx.remove_reaction(reaction.emoji, user)
                self.commands[reaction.emoji]()
                await self.updateMessage()
            except Exception:
                return True
