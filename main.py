# main
import discord
from library import Json, getCurrentTime, existKey
from context import Context
from classes.Club import Club
from classes.Language import Language

# user = UserDiscord
# users = Lista de UserDiscord
# author = UserDicord Que Enviou a Mensagem

# player = Nosso tipo de dado que representa um player
# players = Lista de players
# target = Player que vai sofrer a ação

# guild = Guild do discord
# club = Nosso tipo de dado que representa a guild
# clubs, uma lista de clubs


class Client(discord.Client):
    def __init__(self):
        super().__init__()
        # self.tokens contém os tokens de todos os bots
        self.tokens = Json.loadWrite(pathfile='private/token.json')
        # self.bot contém qual bot está sendo utilizado
        self.bot = "dev"
        self.version = "0.001"
        self.name = "DGBot"
        self.clubs = {}
        # prefixes contém os prefixos de cada club
        self.prefixes = Json.loadWrite(pathfile='private/prefixes.json')
        # languages contém a linguagem selecionada em cada club
        self.languages = Json.loadWrite(pathfile='private/languages.json')
        # langugage contém todas as linguagens
        self.language = Language()
        # roda o client pela chave do token
        self.run(self.tokens[self.bot])

    async def on_ready(self):
        # EVENTO DE QUANDO O BOT ESTA ATIVO
        # pega o tempo atual
        cur_time = getCurrentTime()
        # envia informações da inicialização
        print(f"{self.name} [{self.bot}] - {self.version} init at {cur_time}")
        # informações sobre cada guild
        for guild in self.guilds:
            print(f"\t{guild.name}:{guild.id} connected")

    async def on_message(self, message):
        # EVENTO DE QUANDO UMA MENSAGEM É ENVIADA
        if message.author == self.user:
            # verifica se a mensagem é do proprio bot
            return
        if not message.guild:
            # verifica se a mensagem foi enviada em uma guild
            return
        # recebe o prefixo da guild em questão
        prefix = self.getPrefix(message.guild)
        # instancia um club a partir da guild
        club = self.getClub(message.guild)
        # instancia um objeto contendo as informações do contexto
        context = Context(self, prefix, message)
        # por fim roda o contexto no club criado
        await club.run(context)

    def getClub(self, guild: discord.Guild) -> Club:
        # FUNÇÃO PARA INSTANCIAR UM CLUB
        # cria a chave do club através da guild
        cKey = str(guild.id)
        if not existKey(cKey, self.clubs):
            # se a se esta chave não foi instanciada, faça
            strings = self.getLanguage(guild)
            # instanciando passando a chave e a linguagem
            self.clubs[cKey] = Club(cKey, guild, strings)
        return self.clubs[cKey]

    def getPrefix(self, guild: discord.Guild):
        # DATABASE DOS PREFIXOS
        # cria a chave da guild
        cKey = str(guild.id)
        if not existKey(cKey, self.prefixes):
            # se o prefixo não existir
            return '/'
        else:
            # se existir prefixo, retorne-o
            return self.prefixes[cKey]

    def getLanguage(self, guild: discord.Guild):
        # DATABASE DAS LINGUAGENS
        # cria a chave da guild
        languages = {
            "portuguese": self.language.portuguese
        }
        cKey = str(guild.id)
        if not existKey(cKey, self.languages):
            # se o prefixo não existir
            return languages['portuguese']
        else:
            # se existir prefixo, retorne-o
            return languages[self.languages[cKey]]


client = Client()
