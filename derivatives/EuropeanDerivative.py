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

    def getPrice(self):
        cumulative_payoff = 0
        
        for i in range(self.sample_size):
            previous_simulated_price = self.initial_price
            current_max = float('-inf')
            current_min = float('inf')
            cumulative_price = 0
            average_price = 0
            for j in range(self.time_steps):
                # Get simulated stock price
                Z = np.random.standard_normal()
                exponent = (self.r - self.sigma**2/2)*self.delta_t + self.sigma*np.sqrt(self.delta_t)*Z
                simulated_price = previous_simulated_price*np.exp(exponent)
                #self.simulated_prices[i][j] = simulated_price 
                previous_simulated_price = simulated_price
                # Update minimum and maximum so far
                if simulated_price > current_max: current_max = simulated_price
                if simulated_price < current_min: current_min = simulated_price
                cumulative_price += simulated_price
            # Get maturity value
            average_price = cumulative_price/self.time_steps
            payoff = self.getPayoff(current_min, current_max, simulated_price, self.strike_price, average_price)
            cumulative_payoff += payoff
        # Get sample mean
        average_payoff = cumulative_payoff/self.sample_size
        # Get sample variance
        sample_var = self.initial_price**2*np.exp(2*self.r*self.maturity_duration)*(np.exp(self.sigma**2*self.maturity_duration-1))
        # Return h_bar and 95% confidence interval
        self.price = average_payoff*np.exp(-self.r*self.maturity_duration)
        self.confidence = 1.96*np.sqrt(sample_var/self.sample_size)
        return
    
    def getPayoff(self, min, max, final, strike, average):
        pass