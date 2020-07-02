from classes.Catalog import CatalogAsync


class ItemController(CatalogAsync):
    def __init__(self, club):
        super().__init__(club, name="items")
        self.strings = club.strings.ic
        self.commands = {
            "add item ": self.add_element,
            "new item list ": self.new_datalist,
            "remove item ": self.remove_element,
            "del item list ": self.del_datalist,
            "items": self.send_catalog
        }