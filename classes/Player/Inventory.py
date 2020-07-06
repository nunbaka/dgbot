from classes.MasterBehavior import MasterBehavior
from classes.Database import Datalist, Library
# classe de inventario
# contém listas pre definidas de armazenamento de itens
# não contém protocolo para aceitar dados
# tem função show, função iv
# função show procura no item controller o item
# se o item não for publico ele printa se somente se tiver o item
# função iv printa o que esté no inventário

# player contém o player dono do inventário
# self.ic contém o item controller
# stack, singles
# stacks contém a referncia de itens que existe no item controller
# singles contém itens unicos


class Slot(Datalist):
    def __init__(self, master, key):
        super().__init__(
            master,
            key,
            tKey='_slot',
            default={
                "max_weight": "",
                "currrent_weight": "",
                "max_size": "",
                "current_item": "",
                "requisites": "",
                "item": {}
            })

    def isFree(self):
        pass

    def add_element(self, elm_dict):
        if not self['item']:
            self["item"] = elm_dict
            return True
        return False

    def unequip(self, item):
        pass

    def get(self):
        pass

    def on_equip(self, item):
        pass

    def on_unequip(self, item):
        pass

    def on_get(self):
        pass


class Inventory(Library):
    def __init__(self, master, key):
        super().__init__(master, key)
        self.local += key+'/'
        self.slot_test = Slot(self, "test")
        self.default_slot = ""
        """
        self.weight_capacity
        self.current_weight
        self.default_slot
        self.right_hand_slot
        self.left_hand_slot
        self.pockets_slot
        self.backpack_slot
        self.waist_slot
        self.armor_slot
        self.helmet_slot
        self.quiver_slot
        """

    def add_item_test(self, item):
        self.slot_test.add_element(item)
        self.slot_test.save()

    def new_datalist(self, datalist_name):
        return Slot(self, datalist_name)

    def pick_item(self, slot, item):
        pass

    def drop_item(self, slot, item):
        pass

    def switch_item(self, slot, item):
        pass

    def on_pick_item(self, slot, item):
        pass

    def on_drop_item(self, slot, item):
        pass

    def on_switch_item(self, slot, item):
        pass


class ItemController(Inventory):
    def __init__(self, master, key):
        super().__init__(master, key)
        self.commands = {}
