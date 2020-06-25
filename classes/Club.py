import discord
from library import handleArgs, existKey
from controllers.DiceController import DiceController
from classes.Player import Player
# COMANDOS ESTÃO EM CONTROLLERS

# CLUB:
# players = {}, lista de players, pela chave


class Club:
    def __init__(self, ckey, guild: discord.Guild, strings):
        self.key = ckey
        #self.players = {}
        self.local = f"Clubs/{self.key}/"
        self.guild = guild
        self.strings = strings
        self.dc = DiceController(self)

    async def run(self, context):
        controllers = [self.dc]
        # para cada controller na lista de controllers
        for controller in controllers:
            # para cada comando e função nos comandos do controlador
            for command, function in controller.commands.items():
                content = context.message.content
                prefix = context.prefix
                pKey = str(context.message.author)
                context.setPlayer(self.getPlayer(pKey))
                if content.startswith(prefix+command):
                    # recebe os argumentos, sem o comando
                    content = content[len(prefix+command):]
                    args, comment = handleArgs(content)
                    context.setArgs(args, comment)
                    return await function(context)

    def getPlayer(self, pKey) -> Player:
        if not existKey(pKey, self.players):
            self.players[pKey] = Player(self, pKey)
