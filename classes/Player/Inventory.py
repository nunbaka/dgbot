
from library import existKey
from classes.Datalist import Datalist
from classes.Catalog import Library
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

class Inventory(Library):
    def __init__(self, player, *v, **kv):
        self.player = player
        self.local = player.local+"inventory/"
        
    def find_possible_place(self):
        return self.body
    
    def add_element(self, elm_dict: dict, qtd: int) -> (bool):
        iv = self.find_possible_place()
        try:
            elm_name = elm_dict['msg']['embed']['title']
            elm_id = str.lower(unidecode(elm_dict['msg']['embed']['title']))
            if existKey(elm_id, iv):
                iv[elm_id]['qtd'] += qtd
            else:
                iv.update({elm_id:{
                    "title":elm_name,
                    "qtd":qtd
                    }
                })
            iv.save()
            return True
        except Exception:
            return False