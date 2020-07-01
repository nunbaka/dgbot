from random import randrange
from context import Context
from classes import Club
import re

# nDices = Numero de dados em uma rolagem
# nFaces = Numero de faces de cada dado
# dices = Lista de dados rolados


class Roll:
    def __init__(self,
                 nDices: int,
                 nFaces: int,
                 total: int,
                 dices: list):
        self.nDices = nDices
        self.nFaces = nFaces
        self.total = total
        self.dices = dices


class DiceController:
    def __init__(self, club: Club):
        self.club = club
        self.strings = self.club.strings.dc
        self.commands = {
            'r ': self.r
        }

    async def r(self, context: Context):
        try:
            total, expression = self.getExpression(context.args)
        except Exception:
            await context.sendChannel(self.strings['arg_error'])
            return
        # ENVIANDO UM ROLL, Retornando a mensagem
        return await context.sendChannel(
            self.strings['roll'], total=total, expression=expression)

    def roll(self, nDices: int, nFaces: int) -> Roll:
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
        # TOTAL É A EXPRESSAO SOMENTE COM OS RESULTADOS
        dice_format = self.strings['dice_format']
        total = ""
        # EXPRESSAO É OS ARGUMENTOS TRABALHADOS
        expression = ""
        # O PADRÃO DE UM DADO
        pattern = re.compile('\d*d\d+')
        for arg in args:
            # INCREMENTANDO TOTAL E EXPRESSAO COM O ARGUMENTO
            total += arg+" "
            expression += arg+" "
            dices = pattern.findall(arg)
            # ACHANDO OS PADRÕES DE DADO
            for dice in dices:
                nDices, nFaces = dice.split('d')
                if len(nDices) == 0:
                    nDices = 1
                # ROLANDO O DADO DE CADA OCORRENCIA
                roll = self.roll(int(nDices), int(nFaces))
                # SUBSTITUINDO O ORIGINAL PELO TOTAL
                total = total.replace(dice, str(roll.total), 1)
                # SUBSTITUINDO O ORIGINAL PELO TRATADO
                dicef = dice_format.replace("<#nDices>", str(roll.nDices))
                dicef = dicef.replace("<#nFaces>", str(roll.nFaces))
                dicef = dicef.replace("<#dices>", str(roll.dices))
                dicef = dicef.replace("<#total>", str(roll.total))
                expression = expression.replace(
                    dice, dicef, 1)
        # CALCULANDO A EXPRESSÃO DE TOTAL ENCONTRADA
        total = eval(total)
        return total, expression
