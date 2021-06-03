from EuropeanDerivative import EuropeanDerivative
import numpy as np
import matplotlib.pyplot as plt

class LookbackPut(EuropeanDerivative):
    def getPayoff(self, min, max, final, strike, average):
        payoff = np.max([0, strike-min])
        return payoff
