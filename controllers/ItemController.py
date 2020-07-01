from classes.Catalog import CatalogAsync


class ItemController(CatalogAsync):
    def __init__(self, club):
        super().__init__(club, name="itemController")
        self.strings = club.strings.ic
        self.commands = {
            "add item ": self.add_element,
            "new item list ": self.new_dataList,
            "remove item ": self.remove_element,
            
            "items": self.send_catalog
        }