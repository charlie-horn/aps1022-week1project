from EuropeanDerivative import EuropeanDerivative
import numpy as np

class AsianPut(EuropeanDerivative):
    #def __init__(self):
    #    pass
    def getPayoff(self, min, max, final, strike, average):
        payoff = np.max([strike-average, 0])
        return payoff