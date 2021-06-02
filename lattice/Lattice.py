from math import exp, sqrt, comb

class Lattice:
    def __init__(self, risk_free_rate=0.02, current_price=100, volatility=0.25, strike_price=105, maturity = 2/12, num_steps = 8):
        self.r = risk_free_rate
        self.S_0 = current_price
        self.sigma = volatility
        self.K = strike_price
        self.T = maturity
        self.m = num_steps

        self.u = exp(self.sigma*sqrt(self.T/self.m))
        self.d = exp(-self.sigma*sqrt(self.T/self.m))
        # self.d = 1/self.u
        self.p = (exp(self.r*self.T/self.m) - self.d) / (self.u - self.d)
        return

    def euro_option_pricing(self):
        # # Binomial Distribution for S_T... (obsolete)
        # S_T = [self.S_0 * (self.u**i) * (self.d**(self.m-i)) for i in range(self.m+1)]
        # weights = [comb(self.m, i) * (self.p**i) * ((1-self.p)**(self.m-i)) for i in range(self.m+1)]

        # 1.Exhaustive Attack Method to go through all the possible paths
        S_T = []
        S_max = []
        S_min = []
        weights = []

        for i in range(2**self.m):
            events = '{:08b}'.format(i)
            S = [self.S_0]
            weight = 1
            for char in events:
                if char == '1':
                    S.append(S[-1]*self.u)
                    weight *= self.p
                else:
                    S.append(S[-1]*self.d)
                    weight *= 1-self.p

            S_T.append(S[-1])
            S_max.append(max(S))
            S_min.append(min(S))
            weights.append(weight)

        # pricing
        # Asian call
        future_price = sum([weights[i] * max(S_T[i]-self.K, 0) for i in range(2**self.m)])
        print("--- Asian Call: {}".format(exp(-self.r*self.T/self.m)*future_price))

        # Asian put
        future_price = sum([weights[i] * max(self.K-S_T[i], 0) for i in range(2**self.m)])
        print("--- Asian Put: {}".format(exp(-self.r*self.T/self.m)*future_price))

        # Lookback call
        future_price = sum([weights[i] * max(S_max[i]-self.K, 0) for i in range(2**self.m)])
        print("--- Lookback Call: {}".format(exp(-self.r*self.T/self.m)*future_price))

        # Lookback put
        future_price = sum([weights[i] * max(self.K-S_min[i], 0) for i in range(2**self.m)])
        print("--- Lookback Put: {}".format(exp(-self.r*self.T/self.m)*future_price))

        # Floating lookback call
        future_price = sum([weights[i] * max(S_T[i]-S_min[i], 0) for i in range(2**self.m)])
        print("--- Floating Lookback Call: {}".format(exp(-self.r*self.T/self.m)*future_price))

        # Floating lookback put
        future_price = sum([weights[i] * max(S_max[i]-S_T[i], 0) for i in range(2**self.m)])
        print("--- Floating Lookback Put: {}".format(exp(-self.r*self.T/self.m)*future_price))
        return

    def american_put_pricing(self):
        stock_prices = [[self.S_0]]  # the stock price of all possible time spots

        for time_step in range(1, self.m+1):
            num_events = 2**time_step
            prices_temp = []
            for event in range(num_events):
                if event%2 == 0:
                    prices_temp.append(stock_prices[time_step - 1][event // 2] * self.u)
                else:
                    prices_temp.append(stock_prices[time_step - 1][event // 2] * self.d)
            stock_prices.append(prices_temp)

        option_prices = [] # the option price of all possible time spots

        # when m = T, the price is the payoff
        prices_temp = []
        for event in range(2**self.m):
            prices_temp.append(max(0, self.K - stock_prices[self.m][event]))
        option_prices.append(prices_temp)

        # otherwise, the price is the max of payoff at m or the PV of expected price at m+1,
        for time_step in reversed(range(0, self.m)):
            prices_temp = []
            num_events = 2**time_step
            for event in range(num_events):
                execution_profit = max(0, self.K - stock_prices[time_step][event])
                holding_profit = exp(-self.r*self.T/self.m) * (self.p*option_prices[0][2*event] + (1-self.p)*option_prices[0][2*event+1])
                prices_temp.append(max(execution_profit, holding_profit))
            option_prices.insert(0, prices_temp)

        print("--- American Put: {}".format(option_prices[0][0]))