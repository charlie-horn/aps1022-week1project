from EuropeanDerivative import EuropeanDerivative
import numpy as np

class AsianCall(EuropeanDerivative):
    #def __init__(self):
    #    pass
    def getPayoff(self, min, max, final, strike, average):
        payoff = np.max([0, average - strike])
        return payoff