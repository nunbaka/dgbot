import discord
from library import Json, getCurrentTime

#user = UserDiscord
#users = Lista de UserDiscord
#author = UserDicord Que Enviou a Mensagem

#player = Nosso tipo de dado que representa um player
#players = Lista de players
#target = Player que vai sofrer a ação

#guild = Guild do discord
#club = Nosso tipo de dado que representa a guild

class Client(discord.Client):
    def __init__(self):
        super().__init__()
        self.tokens = Json.loadWrite(pathfile='private/token.json')
        self.bot = "dev"
        self.version = "0.001"
        self.name = "DGBot"
        self.guildManagers = {}
        self.prefixes = Json.loadWrite(pathfile='private/prefixes.json')
        self.run(self.tokens[self.bot])

    async def on_ready(self):
        cur_time = getCurrentTime()
        print(f"{self.name} [{self.bot}] - {self.version} init at {cur_time}")
        for guild in self.guilds:
            print(f"\t{guild.name}:{guild.id} connected")

    async def on_message(self, message):
        if message.author == self.user:
            return
        if not message.guild:
            return

client = Client()
