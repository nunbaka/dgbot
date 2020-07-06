from classes.Database import Element, Datalist, Library
# para criar um controller de biblioteca
# precisa-se criar as 3 bases

# biblioteca: catalogo de datalists
# datalist: catalogo de elementos
# element: o elemento propriamente dito


class StatusElement(Element):
    def __init__(self, elm_dict={}):
        super().__init__(elm_dict)
        self.heart = '❤'
        self.half_heart = '💔'
        self.empty = '🤍'

    def percent(self):
        metadata = self['metadata']
        if metadata['max'] != 0:
            return metadata['value']/metadata['max']*100
        return 100

    def hearts(self):
        p = int(self.percent())
        integer = int(p/10)
        decimal = p-integer*10
        msg_heart = ""
        if integer != 0:
            msg_heart = f"{self.heart*integer}"
        rest = abs(integer-10)
        msg_h_heart = ""
        if decimal != 0:
            rest -= 1
            msg_h_heart = f"{self.half_heart}"
        msg_empty = ""
        if rest != 0:
            msg_empty = f"{self.empty*rest}"
        return f"{msg_heart}{msg_h_heart}{msg_empty}"

    def getMessage(self):
        message = super().getMessage()
        message.setContent(self.hearts())
        return message


class StatusList(Datalist):
    def __init__(self, *v, **kv):
        super().__init__(*v, **kv)

    def new_element(self, elm_dict) -> (StatusElement):
        return StatusElement(elm_dict)


class StatusController(Library):
    def __init__(self, master, key):
        super().__init__(master, key)
        self.strings = self.master.strings.ssc
        self.commands = {
            "new status list ": self.create_datalist,
            "del status list ": self.remove_datalist,
            "create status ": self.create_element,
            "remove status ": self.remove_element,
            "show status ": self.show_element,
            "status ": self.show_element_by_name,
            "show statuss ": self.show_datalist,
            "statuss": self.show_catalog
        }

    def new_datalist(self, datalist_name):
        return StatusList(self, datalist_name)
