import numpy as np
import matplotlib.pyplot as plt

class Asset():
    def __init__(self, initial_price, r, sigma, time_steps, maturity_duration, name):
        self.initial_price = initial_price
        self.r = r
        self.sigma = sigma
        self.price = initial_price
        self.previous_price = initial_price
        self.num_plot_samples = 20
        self.time_steps = time_steps
        self.prices = np.ones((self.num_plot_samples, self.time_steps+1))*initial_price
        self.maturity_duration = maturity_duration
        self.delta_t = maturity_duration/time_steps
        self.name = name
        return

    def simulatePrice(self, sample_id, t):
        Z = np.random.standard_normal()
        exponent = (self.r - self.sigma**2/2)*self.delta_t + self.sigma*np.sqrt(self.delta_t)*Z
        #print(exponent)
        simulated_price = self.previous_price*np.exp(exponent)
        self.price = simulated_price
        self.previous_price = simulated_price
        if sample_id < self.num_plot_samples:
            self.prices[sample_id,t+1] = simulated_price
        return simulated_price

    def plotPrices(self, tau=None):
        for i in range(self.num_plot_samples):
            if self.name == "european":
                self.plot = plt.plot(self.prices[i])
            if tau:
                if tau[0][i]< 7:
                    self.plot = plt.plot(self.prices[i])
        if tau:
            indices = tau[0]
            values = tau[1]
            min_ind = int(np.min(indices))
            max_ind = int(np.max(indices))
            sorted_indices = range(min_ind+1, max_ind+2)
            max_values = np.zeros((max_ind-min_ind+1,1))
            #counts = np.zeros((max_ind-min_ind+1,1))
            for i, value in enumerate(values):
                if max_values[int(indices[i]-min_ind)] < value:
                    max_values[int(indices[i]-min_ind)] = value
                #counts[int(indices[i]-min_ind)] += 1
            #print(sorted_values)
            #print(counts)
            #print(mean_vals)
            plt.plot(sorted_indices, max_values, label="Black-Scholes Barrier", color='green', linewidth=4, alpha=0.7)
            #plt.scatter(indices,values)
            #plt.plot(105)
            plt.legend()
        plt.title("Price simulation")
        plt.ylabel("Stock Price")
        plt.xlabel("Time step")
        plt.savefig(self.name + "_prices.png")
        plt.close()
        return

    def lockPrice(self, sample_id):
        if sample_id < self.num_plot_samples:
            i = 1
            while(self.prices[sample_id,-i]==100):
                self.prices[sample_id,-i] = self.price
                i += 1
        return