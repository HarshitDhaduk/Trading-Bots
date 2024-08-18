'''
my strat -
     - look at the daily resistance on the id
     - and then watch the 1 hour breakout, on close of a 1 hour breakout...place orders between the resistance and the breakout point
     - ATR as the stop loss

'''

import pandas as pd
from backtesting import Backtest, Strategy
from backtesting.lib import SignalStrategy, crossover
from backtesting.test import SMA

#Load daily data
daily_data_path = '/Users/md/Dropbox/dev/github/hyper-liquid-trading-bots/data/WIF_1d_5000.csv'
daily_data = pd.read_csv(daily_data_path, parse_dates=['timestamp'])

# Load hourly data
hourly_data_path= '/Users/md/Dropbox/dev/github/hyper-Liquid-trading-bots/data/WIF_th_5000.csv'
hourly_data = pd.read_csv(hourly_data_path, parse_dates=['timestamp'])


#Ensure the columns are correctly loaded
print(daily_data.columns)
print(hourly_data.columns)

# Set indices for daily and hourly data
daily_data.set_index('timestamp', inplace = True)
hourly_data.set_index('timestamp', inplace = True)

# Rename columns to match the expected format for backtesting.py
hourly_data.rename(columns={
    'open': 'Open',
    'high': 'High',
    'low' : 'Low',
    'close': 'Close',
    'volume': 'Volume'
    
}, inplace = True)

class BreakoutStrategy(Strategy):
    sl_percent = 10  # Default stop loss at 10% 
    tp_percent = 20 # Default take profit at 20%

    def init(self):
        self.daily_resistance = daily_data['resis']

    def next(self):
        # Get the most recent daily resistance level for the current timestamp
        current_time = self.data.index[-1]
        daily_resistance = self.daily_resistance[self.daily_resistance.index <= current_time]
        current_close = self.data.Close[-1]

        # Debug statements to log the resistance and current close price
        print(f"Timestamp: {current_time}")
        print(f"Daily Resistance: {daily_resistance}")
        print(f"Hourly Close: {current_close}")

        # Check for preakout en the hourly tata
        if current_close > daily_resistance:
            entry_price = current_close # Use current close price as entry price
            stop_loss = entry_price * (1 - self.sl_percent / 100)    # Stop loss based on sl_percent
            take_profit = entry_price * (1 + self.tp_percent / 100)  # Take profit based on tp_percent

            # Check if Sl < entry_price < TP 
            if stop_loss < entry_price < take_profit: 
                # Debug statements to ing the breakout condition and order details
                print("Breakout detected at {current_time}")
                print("Entry Price: {entry_price}")
                print("Stop Loss: {stop_loss}")
                print("Take Profit: {take_profit}")

                self.buy(sl=stop_loss, tp=take_profit)

# Ensure the renamed data is correct
print(hourly_data.head())

# Run the backtest
bt = Backtest(hourly_data, BreakoutStrategy, cash=100000, commission= .002)
stats = bt.run()
bt.plot()

# Print the stats
print(stats)


# Optimize the Strategy
opt_stats = bt.optimize(sl_percent = (3, 21, 1), tp_percent = (3, 21, 1), maximize='Equity Final [$]') 
print(opt_stats)