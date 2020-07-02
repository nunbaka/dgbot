from classes.Catalog import CatalogAsync

class SkillController(CatalogAsync):
    def __init__(self, club):
        super().__init__(club, name="skillController")
        self.strings = club.strings.ic
        self.commands = {
            "add skill ": self.add_element,
            "new skill list ": self.new_datalist,
            "remove skill ": self.remove_element,
            
            "skills": self.send_catalog
        }