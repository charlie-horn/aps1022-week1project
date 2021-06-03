from Lattice import  Lattice
import matplotlib.pyplot as plt

project = Lattice(risk_free_rate=0.02,
                  current_price=100,
                  volatility=0.25,
                  strike_price=105,
                  maturity = 2/12,
                  num_steps = 8)
project.euro_option_pricing()
holding_boundary, execution_boundary = project.american_put_pricing()

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
