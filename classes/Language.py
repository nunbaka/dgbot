from library import Json


class Language:
    def __init__(self):
        self.portuguese = Strings("languages/portuguese/")


class Strings:
    def __init__(self, local):
        self.dc = Json.loadWrite(pathfile=local+"DiceController.json")
