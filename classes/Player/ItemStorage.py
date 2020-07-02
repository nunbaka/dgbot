
from library import existKey
from classes.Catalog import Catalog

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

class ItemStorage(Catalog):
    def __init__(self, *v, **kv):
        super().__init__(*v, **kv)
        if not existKey("single", self):
            self.new_datalist('single')
        if not existKey("stack", self):
            self.new_datalist('stack')