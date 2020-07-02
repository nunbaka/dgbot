from classes.Catalog import Library

class SkillController(Library):
    def __init__(self, club):
        super().__init__(club, name="skills")
        self.strings = club.strings.ic
        self.commands = {
            "add skill ": self.add_element,
            "new skill list ": self.new_datalist,
            "remove skill ": self.remove_element,
            "del skill list ": self.del_datalist,
            "skills": self.send_catalog
        }