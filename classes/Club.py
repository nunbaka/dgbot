import discord
from library import handleArgs
from controllers import DiceController

# COMANDOS ESTÃO EM CONTROLLERS


class Club:
    def __init__(self, ckey, guild: discord.Guild, strings):
        self.key = ckey
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
                if content.startswith(prefix+command):
                    # recebe os argumentos, sem o comando
                    content = content[len(prefix+command):]
                    args, comment = handleArgs(content)
                    context.setArgs(args, comment)
                    return await function(context)
