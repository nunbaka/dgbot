

class Inventory(dict):
    def __init__(self, player):
        super().__init__()
        self.player = player
