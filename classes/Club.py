from library import handleArgs

#COMANDOS ESTÃO EM CONTROLLERS

class Club:
    def __init__(self, ckey):
        self.key = ckey
        self.dc 
        
    async def run(self, context):
        controllers = []
        for controller in controllers:
            for command, function in controller.commands.items():
                content = context.message.content
                prefix = context.prefix
                if content.startswith(prefix+command):
                    #recebe os argumentos, sem o comando
                    args = content[len(prefix+command):].split()
                    args, comment = handleArgs(args)
                    context.setArgs(args, comment)
                    return await function(context)