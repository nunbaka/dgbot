from classes.Catalog import Library

class SkillController(Library):
    def __init__(self, club):
        self.strings = club.strings.ic
        self.commands = {
        }