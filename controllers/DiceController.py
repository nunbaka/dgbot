
class DiceController:
    def __init__(self, club):
        self.club = club
        self.commands = {
            'r':self.r
        }
    
    async def r(self, context):
        await context.sendChannel(str(context.args)+"\n"+context.comment)
        