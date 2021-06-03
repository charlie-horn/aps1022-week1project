import os
import sys
import inspect
import numpy as np
from numpy.lib.function_base import percentile

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir+"/derivatives") 

from AsianCall import AsianCall
from AsianPut import AsianPut
from FloatingLookbackCall import FloatingLookbackCall
from FloatingLookbackPut import FloatingLookbackPut
from LookbackCall import LookbackCall
from LookbackPut import LookbackPut
from Asset import Asset

from AmericanPut import AmericanPut

class MonteCarlo():
    def __init__(self, sample_size, time_steps, initial_price, r, sigma, maturity_duration, strike_price):
        self.sample_size = sample_size
        self.time_steps = time_steps
        self.strike_price = strike_price
        self.T = maturity_duration
        self.europeanAsset = Asset(initial_price, r, sigma, time_steps, maturity_duration, "european")
        self.europeanDerivatives = {"asianCall" : AsianCall(sample_size, time_steps, initial_price, r, sigma, maturity_duration, strike_price),
                            "asianPut" : AsianPut(sample_size, time_steps, initial_price, r, sigma, maturity_duration, strike_price),
                            "floatingLookbackCall" : FloatingLookbackCall(sample_size, time_steps, initial_price, r, sigma, maturity_duration, strike_price),
                            "floatingLookbackPut" : FloatingLookbackPut(sample_size, time_steps, initial_price, r, sigma, maturity_duration, strike_price),
                            "lookbackCall" : LookbackCall( sample_size, time_steps, initial_price, r, sigma, maturity_duration, strike_price),
                            "lookbackPut" : LookbackPut(sample_size, time_steps, initial_price, r, sigma, maturity_duration, strike_price)}
        self.americanAsset = Asset(initial_price, r, sigma, time_steps, maturity_duration, "american")
        self.americanDerivatives = {"americanPut" : AmericanPut(sample_size, time_steps, initial_price, r, sigma, maturity_duration, strike_price)}
        self.getEuropeanPrices()
        self.getAmericanPrices()

    def getAmericanPrices(self):
        for derivative in self.americanDerivatives.values():
            cumulative_payoff = 0
            tau = np.zeros(self.sample_size)
            tau_vals = np.zeros(self.sample_size)
            for i in range(self.sample_size):
                previous_simulated_price = derivative.initial_price
                current_max = float('-inf')
                current_min = float('inf')
                cumulative_price = 0
                average_price = 0
                found_optimal_stopping_time = False
                for j in range(self.time_steps):
                    if found_optimal_stopping_time: break
                    t = j*self.T/self.time_steps
                    K = derivative.strike_price
                    simulated_price = self.americanAsset.simulatePrice(i, j)
                    d1 = (np.log(simulated_price/K)+(derivative.r+derivative.sigma**2/2)*(self.T-t))/(derivative.sigma*np.sqrt(self.T-t))
                    #print("d1:",d1)
                    d2 = d1 - derivative.sigma*np.sqrt(self.T-t)
                    #print("d2:",d2)
                    #previous_simulated_price = simulated_price
                    BS_price = derivative.getBlackScholes(simulated_price, t, d1, d2)
                    payoff = derivative.getPayoff(current_min, current_max, simulated_price, derivative.strike_price, average_price)
                    price = payoff*np.exp(-self.americanAsset.r*t)
                    if payoff >= BS_price: 
                        #print("------", j)
                        #print("Current price is:", price)
                        #print("BS model says:", BS_price)
                        derivative.payoffs = np.append(derivative.payoffs, payoff)
                        cumulative_payoff += payoff
                        tau[i] = j#t
                        tau_vals[i] = simulated_price
                        self.americanAsset.lockPrice(i)
                        break
                    if j == self.time_steps - 1:
                        cumulative_payoff += payoff
                        derivative.payoffs = np.append(derivative.payoffs, payoff)
                        tau[i] = j#derivative.maturity_duration
                        tau_vals[i] = simulated_price
                        break
            mean_stopping_time = np.mean(tau)
            variance_stopping_time = np.var(tau)
            derivative.stopping_time = mean_stopping_time
            average_payoff = cumulative_payoff/self.sample_size
            derivative.price = average_payoff*np.exp(-derivative.r*mean_stopping_time)
            #sample_var = derivative.getVariance()
            derivative.confidence =  1.96*np.sqrt(np.var(derivative.payoffs)/self.sample_size)
        self.americanAsset.plotPrices(tau=(tau, tau_vals))
        return

    def getEuropeanPrices(self):
        
        for i in range(self.sample_size):
            current_max = float('-inf')
            current_min = float('inf')
            cumulative_price = 0
            average_price = 0
            for j in range(self.time_steps):
                # Get simulated stock price
                simulated_price = self.europeanAsset.simulatePrice(i, j)
                # Update minimum and maximum so far
                if simulated_price > current_max: current_max = simulated_price
                if simulated_price < current_min: current_min = simulated_price
                cumulative_price += simulated_price
            # Get maturity value
            average_price = cumulative_price/self.time_steps
            for derivative in self.europeanDerivatives.values():
                payoff = derivative.getPayoff(current_min, current_max, simulated_price, self.strike_price, average_price)
                derivative.payoffs = np.append(derivative.payoffs, payoff)
                derivative.cumulative_payoff += payoff
        self.europeanAsset.plotPrices()

        for derivative in self.europeanDerivatives.values():
            # Get sample mean
            derivative.average_payoff = np.mean(derivative.payoffs) #derivative.cumulative_payoff/self.sample_size
            # Get sample variance
            sample_var = np.var(derivative.payoffs) #self.europeanAsset.initial_price**2*np.exp(2*self.europeanAsset.r*self.europeanAsset.maturity_duration)*(np.exp(self.europeanAsset.sigma**2*self.europeanAsset.maturity_duration-1))
            # Return h_bar and 95% confidence interval
            derivative.price = derivative.average_payoff*np.exp(-self.europeanAsset.r*self.europeanAsset.maturity_duration)
            derivative.confidence = 1.96*np.sqrt(sample_var/self.sample_size)

        return
