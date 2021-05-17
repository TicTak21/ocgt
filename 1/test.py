from HookeJeeves import hooke_jeeves
from decimal import Decimal
from numpy import round
from math import *
import math


class hooke_jeeves_executor:
    def __init__(self, f, stt, amount):
        self.f = f
        self.stt = stt
        self.amount = amount

    # parse string and convert it to the function
    def getValueofFunction(self, x, n):
        # dict = {'x': x}

        f = self.f
        # print(f, type(f))
        r = eval(f, {"tan": tan, "exp": exp, "x": x})
        # print(r)
        return r

    def run(self):
        txtTau = 0.5
        txtEps = Decimal("1.0E-7")

        it, endpt, points = hooke_jeeves(
            self.amount, self.stt, txtTau, txtEps, 1000, self.getValueofFunction
        )
        # print([txtX, txtY], txtTau, txtEps, 1000, self.getValueofFunction)
        endpt_rounded = round(endpt, 2)
        print("Iterations = ", it, " end pt : ", endpt_rounded)


# f2
f = "(10*(x[0] - x[1])**2 + (x[0] - 1)**2)**4"

# x^(0)
stt = [-1.2, 0.0]

# number of points
amount = 2

exec1 = hooke_jeeves_executor(f, stt, amount)
exec1.run()
# ----------------------

# f6
f = "exp(x[0] - x[1])**4 + 100*(x[1] -x[2])**6 + tan(x[2] -x[3])**4 + x[0]**8 + (x[3]-1)**2"

# x^(0)
stt = [1.0, 2.0, 2.0, 2.0]

# number of points
amount = 4

exec2 = hooke_jeeves_executor(f, stt, amount)
exec2.run()