from numpy.lib.nanfunctions import _nanmedian1d
from EuropeanDerivative import EuropeanDerivative
import numpy as np
from scipy.stats import norm

class AmericanPut(EuropeanDerivative):
    def getPayoff(self, min, max, final, strike, average):
        payoff = np.max([0, strike - final])
        return payoff

    def getBlackScholes(self, previous_price, t, d1, d2):
        T = self.maturity_duration
        K = self.strike_price
        r = self.r
        N1 = norm.pdf(-d1)
        N2 = norm.pdf(-d2)
        expected_price = K*np.exp(-r*(T-t))*N2 - previous_price*N1
        return expected_price

    def getVariance(self):
        variance = self.initial_price**2*np.exp(2*self.r*self.maturity_duration)*(np.exp(self.sigma**2*self.maturity_duration-1))
        return variance