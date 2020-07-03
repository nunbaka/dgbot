from classes.Library import Library


class ItemController(Library):
    def __init__(self, club):
        super().__init__(club, name="items")
        self.club = club
        self.strings = club.strings.ic
        self.commands = {
            "add list item": self.add_datalist,
            "remove list item ": self.remove_datalist,
            "add item ": self.add_element,
            "remove item ": self.remove_element,
            "items": self.send_catalog,
            "give item ": self.give,
            "iv": self.show_inventory
        }

    async def show_inventory(self, context):
        user = context.author
        player = self.club.getPlayer(user)
        await context.channel.send(player.inventory.body)
        return True

    async def give(self, context):
        # argumentos:
        # @user item_name qtd
        try:
            # recebendo o user
            user = context.users[0]
            player = self.club.getPlayer(user)
            if not player:
                print("player sem ficha")
                return None
        except Exception as inst:
            print("Necessita mencionar o user no primeiro argumento", inst)
            return None
        try:
            # recebendo o nome do item
            elm_name = context.args[1]
        except Exception:
            print("Necessita informar o nome do item corretamente")
            return None
        try:
            qtd = int(context.args[2])
        except Exception:
            qtd = 1
        # ao chegar aqui significa que os argumentos
        #  foram minimamente informados
        try:
            elm, datalist_id = self.get_element_by_name(elm_name)
            player.inventory.add_element(elm, qtd)
        except Exception:
            print("Elemento inexistente")
            return None
