from library import handleArgs, existKey
from controllers.DiceController import DiceController
from controllers.ItemController import ItemController
from controllers.StatusController import StatusController
from classes.player.Inventory import Inventory
from classes.MasterBehavior import MasterBehavior, Event
# COMANDOS ESTÃO EM CONTROLLERS

# CLUB:
# players = {}, lista de players, pela chave


class Player(MasterBehavior):
    def __init__(self, *v, **kv):
        super().__init__(*v, **kv)
        self.strings = self.master.strings.p
        self.local += f"players/{self.key}/"
        self.inventory = Inventory(self, "Inventory")
        # self.spells = Spell()

    def getCommands(self):
        cmds = {}
        return cmds


class Club(MasterBehavior):
    def __init__(self, master, key, strings):
        self.strings = strings
        super().__init__(master, key)
        self.local += f"Clubs/{self.key}/"
        self.players: dict = dict()
        self.ic = ItemController(
            self, "ItemController")
        self.dc = DiceController(
            self, "DiceController")
        self.ssc = StatusController(
            self, "StatusController")

    async def run(self, event: Event):
        controllers = [self.dc, self.ic, self.ssc]
        # para cada controller na lista de controllers
        event.club = self
        content: str = event.message.content
        prefix = event.prefix
        event_prefix = event.event_prefix
        for controller in controllers:
            # para cada comando e função nos comandos do controlador
            for command, function in controller.commands.items():
                if content.startswith(prefix+command):
                    # recebe os argumentos, sem o comando
                    content = content[len(prefix+command):]
                    args, comment = handleArgs(content)
                    event.args = args
                    event.comment = comment
                    return await function(event)
        player = self.getPlayer(event.author)
        event.player = player
        if content.startswith(event_prefix):
            print("Começa com prefixo")

    def getPlayer(self, user) -> Player:
        key = str(user.id)
        if not existKey(key, self.players):
            self.players[key] = Player(self, key)
        return self.players[key]
