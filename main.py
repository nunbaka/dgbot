# main
import discord
from library import Json, getCurrentTime, existKey
from classes.MasterBehavior import Event
from classes.Language import Language
from classes.Club import Club


# user = UserDiscord
# users = Lista de UserDiscord
# author = UserDicord Que Enviou a Mensagem

# player = Nosso tipo de dado que representa um player
# players = Lista de players
# target = Player que vai sofrer a ação

# guild = Guild do discord
# club = Nosso tipo de dado que representa a guild
# clubs, uma lista de clubs
"""
    +Club:
        +Armazenamento de players
            +GetPlayer user
        +Armazenamento de items
            +give @user name_id qtd=1 / to player
                -change to +give item
            +list datalist / view a datalist of items
            +new datalist datalist_id / add a new datalist
            +add datalist #item/ add a item on datalist
            -del datalist datalist_id/ delete a datalist
            -remove datalist item / remove item from datalist
        -Armazenamento de Skills
            -give skill @user name_id / give a skill
            -list datalist name_id / view a datalist of skills
            -new datalist datalist_id /
            -add datalist #skill
            -del datalist datalist_id
            -remove datalist item / remove item from datalist
        -Armazenamento de terrenos
            -set @channel terrain_id / set terrain
            -terrain @terrain / Show Stats of Terrain
            -Shop:
                -shop / view the shop catalog
                -buy name_id qtd = 1 / buy itemg
                -sell name_id qtd = 1 / sell item
                -cheat
        +Controle de Dados
            +roll dice
    +Player:
        +Inventory:
            +iv / show all inventory
                -change to +items
            +show name_id / show item
                -change to +item name_id
        -Skill:
            -skill name_id / show the skill
            -skills / show the skills
        -Economy:
            -money / MONEY
            -bank / MONEY (in bank)
            -trade @player / Trade Event
"""


class Client(discord.Client):
    def __init__(self):
        super().__init__()
        # self.tokens contém os tokens de todos os bots
        self.tokens = Json.loadWrite(pathfile='private/token')
        # self.bot contém qual bot está sendo utilizado
        self.bot = "dev"
        self.version = "0.001"
        self.name = "DGBot"
        self.local = "private/"
        self.clubs = {}
        # prefixes contém os prefixos de cada club
        self.prefixes = Json.loadWrite(pathfile='private/prefixes')
        self.event_prefixes = Json.loadWrite(pathfile='private/event_prefixes')
        # languages contém a linguagem selecionada em cada club
        self.languages = Json.loadWrite(pathfile='private/languages')
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
        event_prefix = self.getEventPrefix(message.guild)
        # instancia um club a partir da guild
        club = self.getClub(message.guild)
        # instancia um objeto contendo as informações do contexto
        # por fim roda o contexto no club criado
        await club.run(Event(self, prefix, event_prefix, message))

    def getClub(self, guild: discord.Guild) -> (Club):
        # FUNÇÃO PARA INSTANCIAR UM CLUB
        # cria a chave do club através da guild
        key = str(guild.id)
        if not existKey(key, self.clubs):
            # se a se esta chave não foi instanciada, faça
            strings = self.getLanguage(guild)
            # instanciando passando a chave e a linguagem
            self.clubs[key] = Club(self, key, strings)
        return self.clubs[key]

    def getEventPrefix(self, guild: discord.Guild):
        # DATABASE DOS PREFIXOS
        # cria a chave da guild
        cKey = str(guild.id)
        if not existKey(cKey, self.event_prefixes):
            # se o prefixo não existir
            return '!'
        else:
            # se existir prefixo, retorne-o
            return self.prefixes[cKey]

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
