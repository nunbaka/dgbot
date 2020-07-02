from classes.Catalog import CatalogAsync

class SkillController(CatalogAsync):
    def __init__(self, club):
        super().__init__(club, name="skillController")
        self.strings = club.strings.ic
        self.commands = {}