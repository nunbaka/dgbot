import discord
from library import handleArgs, existKey
from controllers.DiceController import DiceController
from controllers.ItemController import ItemController
from controllers.SkillController import SkillController
from classes.player.Inventory import Inventory
# COMANDOS ESTÃO EM CONTROLLERS

# CLUB:
# players = {}, lista de players, pela chave


class Player:
    def __init__(self, club, pKey):
        self.club = club
        self.strings = self.club.strings.p
        self.key = pKey
        self.local = f"{club.local}players/{pKey}/"
        self.inventory = Inventory(self)
        # self.spells = Spell()

    def getCommands(self):
        cmds = {}
        return cmds


class Club:
    def __init__(self, ckey, guild: discord.Guild, strings):
        self.key = ckey
        self.players: dict = dict()
        self.local = f"Clubs/{self.key}/"
        self.guild = guild
        self.strings = strings
        self.dc = DiceController(self)
        self.ic = ItemController(self)
        self.sc = SkillController(self)

    async def run(self, context):
        controllers = [self.dc, self.ic, self.sc]
        # para cada controller na lista de controllers
        content = context.message.content
        prefix = context.prefix
        for controller in controllers:
            # para cada comando e função nos comandos do controlador
            for command, function in controller.commands.items():
                if content.startswith(prefix+command):
                    # recebe os argumentos, sem o comando
                    content = content[len(prefix+command):]
                    args, comment = handleArgs(content)
                    context.args = args
                    context.comment = comment
                    context.club = self
                    return await function(context)
        context.player = self.getPlayer(context.message.author)
        for command, function in context.player.getCommands().items():
            if content.startswith(prefix+command):
                content = content[len(prefix+command):]
                args, comment = handleArgs(content)
                context.args = args
                context.comment = comment
                context.club = self
                return await function(context)

    def getPlayer(self, user) -> Player:
        pKey = str(user.id)
        if not existKey(pKey, self.players):
            self.players[pKey] = Player(self, pKey)
        return self.players[pKey]
