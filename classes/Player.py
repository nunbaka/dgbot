from classes.Club import Club
from classes.p.Inventory import Inventory


class Player:
    def __init__(self, club: Club, pKey):
        self.club = club
        self.key = pKey
        self.local = f"{club.local}players/{pKey}/"
        self.inventory = Inventory(self)
