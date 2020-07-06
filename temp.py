
class Status:
    def __init__(self, value=0, min=0, max=0):
        self.value = value
        self.max = max
        self.min = min
        self.heart = '❤'
        self.half_heart = '💔'
        self.empty = '🤍'

    def percent(self):
        if max != 0:
            return self.value/self.max*100
        return 100

    def __str__(self):
        p = int(self.percent())
        integer = int(p/10)
        decimal = p-integer*10
        print("integer: ", integer, "decimal: ", decimal)
        msg_heart = ""
        if integer != 0:
            msg_heart = f"{self.heart*integer}"
        rest = abs(integer-10)
        msg_h_heart = ""
        if decimal != 0:
            rest -= 1
            msg_h_heart = f"{self.half_heart}"
        msg_empty = ""
        if rest != 0:
            msg_empty = f"{self.empty*rest}"
        return f"{msg_heart}{msg_h_heart}{msg_empty}"


f = Status(45, 0, 100)

print(f)
