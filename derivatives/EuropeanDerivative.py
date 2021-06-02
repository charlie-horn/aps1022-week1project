import numpy as np

class EuropeanDerivative():
    def __init__(self, sample_size, time_steps, initial_price, r, sigma, maturity_duration, strike_price):
        self.sample_size = sample_size
        self.time_steps = time_steps
        self.initial_price = initial_price
        self.r = r
        self.sigma = sigma
        self.maturity_duration = maturity_duration
        self.delta_t = maturity_duration/time_steps
        self.strike_price = strike_price
        return

    def simulatePrice(self, previous_simulated_price):
        Z = np.random.standard_normal()
        exponent = (self.r - self.sigma**2/2)*self.delta_t + self.sigma*np.sqrt(self.delta_t)*Z
        simulated_price = previous_simulated_price*np.exp(exponent)
        return simulated_price
    
    def getPayoff(self, min, max, final, strike, average):
        pass