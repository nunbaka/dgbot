from library import Json


class Language:
    def __init__(self):
        self.portuguese = Strings("languages/portuguese/")


class Strings:
    def __init__(self, local):
        self.dc = Json.loadWrite(pathfile=local+"DiceController.json")
        self.ic = Json.loadWrite(pathfile=local+"ItemController.json")
        self.p = Json.loadWrite(pathfile=local+"Player.json")
