from Lattice import  Lattice
import matplotlib.pyplot as plt

project = Lattice(risk_free_rate=0.02,
                  current_price=100,
                  volatility=0.25,
                  strike_price=105,
                  maturity = 2/12,
                  num_steps = 8)

asian_call_price, asian_put_price, lookback_call_price, lookback_put_price, floating_lookback_call, floating_lookback_put = project.euro_option_pricing()

print("--- Asian Call: {}".format(asian_call_price))
print("--- Asian Put: {}".format(asian_put_price))
print("--- Lookback Call: {}".format(lookback_call_price))
print("--- Lookback Put: {}".format(lookback_put_price))
print("--- Floating Lookback Call: {}".format(floating_lookback_call))
print("--- Floating Lookback Put: {}".format(floating_lookback_put))

price, avg_optimal_time, holding_boundary, execution_boundary = project.american_put_pricing()
print("--- American Put Price: {}".format(price))
print("--- American Put Average Stopping Time: {}".format(avg_optimal_time))

# make a plot
x1 = [i for i in range(1,8)]
x2 = [i for i in range(3,8)]

fig, ax = plt.subplots()
fig.set_size_inches(9, 6)
ax.plot(x1, holding_boundary)
ax.plot(x2, execution_boundary[2:])
ax.set(xlabel='time (steps)',
       ylabel='asset price (USD)',
       xlim=[0, 8],
       ylim=[85, 115])
ax.legend(['Holding', 'Exercising'])
ax.grid()
plt.show()

# # this is the example of the paper: price: 12.8618; stopping time: 3.25
# example = Lattice(risk_free_rate=0.1,
#                   current_price=100,
#                   volatility=0.34641,
#                   strike_price=110,
#                   maturity = 4/12,
#                   num_steps = 4)
# example.american_put_pricing()
