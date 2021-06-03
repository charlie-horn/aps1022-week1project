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
    print("--- Asian Call: " + str(simulator.europeanDerivatives["asianCall"].price), simulator.europeanDerivatives["asianCall"].confidence)
    print("--- Asian Put: " + str(simulator.europeanDerivatives["asianPut"].price), simulator.europeanDerivatives["asianPut"].confidence)
    print("--- Lookback Call: " + str(simulator.europeanDerivatives["floatingLookbackCall"].price), simulator.europeanDerivatives["floatingLookbackCall"].confidence)
    print("--- Lookback Put: " + str(simulator.europeanDerivatives["floatingLookbackPut"].price), simulator.europeanDerivatives["floatingLookbackPut"].confidence)
    print("--- Floating Lookback Call: " + str(simulator.europeanDerivatives["lookbackCall"].price), simulator.europeanDerivatives["lookbackCall"].confidence)
    print("--- Floating Lookback Put: " + str(simulator.europeanDerivatives["lookbackPut"].price), simulator.europeanDerivatives["lookbackPut"].confidence)
    
     # 1. b)
    print("---------------------")
    print("1. b) Price an American Put option using Monte Carlo Simulation.")
    print("--- American Put: " + str(simulator.americanDerivatives["americanPut"].price), simulator.americanDerivatives["americanPut"].confidence)