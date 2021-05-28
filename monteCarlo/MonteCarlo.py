import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir+"/derivatives") 

from AsianCall import AsianCall
from AsianPut import AsianPut
from FloatingLookbackCall import FloatingLookbackCall
from FloatingLookbackPut import FloatingLookbackPut
from LookbackCall import LookbackCall
from LookbackPut import LookbackPut

class MonteCarlo():
    def __init__(self, sample_size, time_steps, initial_price, r, sigma, maturity_duration, strike_price):
        self.sample_size = sample_size
        self.time_steps = time_steps
        self.europeanDerivatives = {"asianCall" : AsianCall(sample_size, time_steps, initial_price, r, sigma, maturity_duration, strike_price),
                            "asianPut" : AsianPut(sample_size, time_steps, initial_price, r, sigma, maturity_duration, strike_price),
                            "floatingLookbackCall" : FloatingLookbackCall(sample_size, time_steps, initial_price, r, sigma, maturity_duration, strike_price),
                            "floatingLookbackPut" : FloatingLookbackPut(sample_size, time_steps, initial_price, r, sigma, maturity_duration, strike_price),
                            "lookbackCall" : LookbackCall(sample_size, time_steps, initial_price, r, sigma, maturity_duration, strike_price),
                            "lookbackPut" : LookbackPut(sample_size, time_steps, initial_price, r, sigma, maturity_duration, strike_price)}
        self.getEuropeanPrices()

    def getEuropeanPrices(self):
        for derivative in self.europeanDerivatives.values():
            derivative.getPrice()
