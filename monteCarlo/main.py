from MonteCarlo import MonteCarlo

if __name__ == "__main__":
    sample_size = 250
    time_steps = 10
    initial_price = 100
    r = 0.02
    sigma = 0.25
    maturity_duration = 2/12
    strike_price = 105
    simulator = MonteCarlo(sample_size, time_steps, initial_price, r, sigma, maturity_duration, strike_price)
    # 1. a)
    print("---------------------")   
    print("1. a) Compute the price of the following options using Monte Carlo Simulation with the sample size 250 or larger.")
    #simulator.getEuropeanPrices()
    print("--- Asian Call: " + str(simulator.europeanDerivatives["asianCall"].price))
    print("--- Asian Put: " + str(simulator.europeanDerivatives["asianPut"].price))
    print("--- Lookback Call: " + str(simulator.europeanDerivatives["floatingLookbackCall"].price))
    print("--- Lookback Put: " + str(simulator.europeanDerivatives["floatingLookbackPut"].price))
    print("--- Floating Lookback Call: " + str(simulator.europeanDerivatives["lookbackCall"].price))
    print("--- Floating Lookback Put: " + str(simulator.europeanDerivatives["lookbackPut"].price))
    
     # 1. b)
    print("---------------------")