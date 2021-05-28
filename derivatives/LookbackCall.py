from EuropeanDerivative import EuropeanDerivative
import numpy as np

class LookbackCall(EuropeanDerivative):
    #def __init__(self):
    #    pass
    def getPayoff(self, min, max, final, strike, average):
        payoff = np.max([0, max-strike])
        return payoff