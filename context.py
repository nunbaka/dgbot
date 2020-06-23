

class Context:
    def __init__(self, client, prefix, message):
        self.client = client
        self.prefix = prefix
        self.message = message
        self.guild = message.guild
        self.author = message.author
        self.users = message.mentions
    
    def setArgs(self, args, comment):
        self.args = args
        self.comment = comment
        pass