

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

    async def sendChannel(self, message):
        return await self.channel.send(message)

    def sendAuthor(self):
        pass
