from classes.Database import Element, Datalist, Library, Event
# para criar um controller de biblioteca
# precisa-se criar as 3 bases

# biblioteca: catalogo de datalists
# datalist: catalogo de elementos
# element: o elemento propriamente dito


class ItemElement(Element):
    def __init__(self, elm_dict={}):
        super().__init__(elm_dict)


class ItemList(Datalist):
    def __init__(self, *v, **kv):
        super().__init__(*v, **kv)

    def new_element(self, elm_dict) -> (ItemElement):
        return ItemElement(elm_dict)


class ItemController(Library):
    def __init__(self, master, key):
        super().__init__(master, key)
        self.strings = self.master.strings.ic
        self.commands = {
            "new item list ": self.create_datalist,
            "del item list ": self.remove_datalist,
            "create item ": self.create_element,
            "remove item ": self.remove_element,
            "show item ": self.show_element,
            "item ": self.show_element_by_name,
            "show items ": self.show_datalist,
            "items": self.show_catalog,
            "add item ": self.add_item_by_name
        }

    async def add_item_by_name(self, event: Event):
        try:
            event.user = event.users[0]
        except Exception:
            print("user not informed")
            return False
        try:
            target = event.club.getPlayer(event.user)
            inventory = target.inventory
        except Exception:
            print("player não tem ficha")
            return False
        item_name = event.args[1]
        item, datalist_key = self.get_element_by_name(item_name)
        if not item:
            print("sem item")
            return None
        inventory.add_item_test(item)

    def new_datalist(self, datalist_name):
        return ItemList(self, datalist_name)
