from classes.Database import Element, Datalist, Library
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
            "new item list ": self.add_datalist,
            "del item list ": self.remove_datalist,
            "add item ": self.add_element,
            "remove item ": self.remove_element,
            "show item ": self.show_element,
            "item ": self.show_element_by_name,
            "show items ": self.show_datalist,
            "items": self.show_catalog
        }

    def new_datalist(self, datalist_name):
        return ItemList(self, datalist_name)
