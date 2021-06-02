from Lattice import  Lattice
testing = Lattice(risk_free_rate=0.02,
                  current_price=100,
                  volatility=0.25,
                  strike_price=105,
                  maturity = 2/12,
                  num_steps = 8)
testing.euro_option_pricing()
testing.american_put_pricing()