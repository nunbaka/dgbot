from random import randrange
import re

# nDices = Numero de dados em uma rolagem
# nFaces = Numero de faces de cada dado
# dices = Lista de dados rolados


class DiceController:
    def __init__(self, club):
        self.club = club
        self.commands = {
            'r': self.r
        }

    async def r(self, context):
        try:
            total, expression = self.getExpression(context.args)
        except Exception:
            await context.sendChannel("Error na argumentação")
            return
        # ENVIANDO UM ROLL
        await context.sendChannel(
            f"{context.author.mention} rolou {expression}, TOTAL: {total}")

    def roll(self, nDices, nFaces):
        # soma total dos dados
        total = 0
        # lista de dados rolado
        dices = []
        # rolando os dados
        for i in range(nDices):
            v = randrange(1, nFaces+1)
            dices.append(v)
            total += v
        return Roll(nDices, nFaces, total, dices)

    def getExpression(self, args):
        total = ""
        expression = ""
        pattern = re.compile("\d*d\d+")
        for arg in args:
            total += arg+" "
            expression += arg+" "
            dices = pattern.findall(arg)
            for dice in dices:
                nDices, nFaces = dice.split('d')
                if len(nDices) == 0:
                    nDices = 1
                roll = self.roll(int(nDices), int(nFaces))
                total = total.replace(dice, str(roll.total), 1)
                expression = expression.replace(
                    dice,
                    f"{roll.nDices}d{roll.nFaces}, {roll.dices}: {roll.total}", 1)
        total = eval(total)
        return total, expression


class Roll:
    def __init__(self, nDices, nFaces, total, dices):
        self.nDices = nDices
        self.nFaces = nFaces
        self.total = total
        self.dices = dices
