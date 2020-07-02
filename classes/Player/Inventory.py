
from library import existKey
from classes.Datalist import Datalist
from unidecode import unidecode
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

class Inventory(Datalist):
    def __init__(self, *v, **kv):
        super().__init__(*v, **kv)
    def add_element(self, elm_dict: dict, qtd: int) -> (bool):
        try:
            elm_name = elm_dict['msg']['embed']['title']
            elm_id = str.lower(unidecode(elm_dict['msg']['embed']['title']))
            if existKey(elm_id, self):
                self[elm_id]['qtd'] += qtd
                return True
            else:
                self.update({elm_id:{
                    "title":elm_name,
                    "qtd":qtd
                    }
                })
                return False
        except Exception:
            return False