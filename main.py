import discord
from library import Json, getCurrentTime, existKey
from context import Context
from classes.Club import Club

#user = UserDiscord
#users = Lista de UserDiscord
#author = UserDicord Que Enviou a Mensagem

#player = Nosso tipo de dado que representa um player
#players = Lista de players
#target = Player que vai sofrer a ação

#guild = Guild do discord
#club = Nosso tipo de dado que representa a guild
#clubs, uma lista de clubs

class Client(discord.Client):
    def __init__(self):
        super().__init__()
        #self.tokens contém os tokens de todos os bots
        self.tokens = Json.loadWrite(pathfile='private/token.json')
        #self.bot contém qual bot está sendo utilizado
        self.bot = "dev"
        self.version = "0.001"
        self.name = "DGBot"
        self.clubs = {}
        #self.prefixes contém os prefixos de cada club 
        self.prefixes = Json.loadWrite(pathfile='private/prefixes.json')
        #roda o client pela chave do token
        self.run(self.tokens[self.bot])

    async def on_ready(self):
        #pega o tempo atual
        cur_time = getCurrentTime()
        #envia informações da inicialização
        print(f"{self.name} [{self.bot}] - {self.version} init at {cur_time}")
        #informações sobre cada guild
        for guild in self.guilds:
            print(f"\t{guild.name}:{guild.id} connected")

    async def on_message(self, message):
        if message.author == self.user:
            #verifica se a mensagem é do proprio bot
            return
        if not message.guild:
            #verifica se a mensagem foi enviada em uma guild
            return
        #recebe o prefixo da guild em questão
        prefix = self.getPrefix(message.guild)
        #instancia um club a partir da guild
        club = self.getClub(message.guild)
        #instancia um objeto contendo as informações do contexto
        context = Context(self, prefix, message)
        await club.run(context)
    
    def getClub(self, guild):
        #cria a chave da guild
        cKey = str(guild.id)
        if not existKey(cKey, self.clubs):
            #se a chave não existir no dicionario, instancia um club na referencia
            self.clubs[cKey] = Club(cKey)
        return self.clubs[cKey]

    def getPrefix(self, guild):
        #cria a chave da guild
        cKey = str(guild.id)
        if not existKey(cKey, self.prefixes):
            #se o prefixo não existir
            return '/'
        else:
            #se existir prefixo, retorne-o
            return self.prefixes[cKey]

client = Client()
