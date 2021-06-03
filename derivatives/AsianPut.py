from EuropeanDerivative import EuropeanDerivative
import numpy as np
import matplotlib.pyplot as plt

class AsianPut(EuropeanDerivative):
    def getPayoff(self, min, max, final, strike, average):
        payoff = np.max([strike-average, 0])
        return payoff