from classes.Catalog import Library, Catalog


class ItemController(Library):
    def __init__(self, club):
        super().__init__(club, name="items")
        self.club = club
        self.strings = club.strings.ic
        self.commands = {
            "add item ": self.add_element,
            "new item list ": self.new_datalist,
            "remove item ": self.remove_element,
            "del item list ": self.del_datalist,
            "items": self.send_catalog,
            "give item ": self.give,
        }
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
        except Exception:
            print("Necessita mencionar o user no primeiro argumento")
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
        # ao chegar aqui significa que os argumentos foram minimamente informados
        try:
            elm, datalist_id = self.get_element_by_name(elm_name)
        except Exception:
            print("Elemento inexistente")
            return None
        if elm.isSingle():
            player.inventory.add_element('single', elm)
        