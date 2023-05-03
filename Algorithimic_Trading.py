"""
In this Project I will follow NeuralNine tutorial on Algorithmic Trading Strategy
To automatic trade stocks with Python Code.
In the first part of this project i will only follow his code and after that I am going to implement
some personal ideas that I have (For example, send email messages to warn about the stock)
The next step is to organize the Code with functions and classes to make it prettier and more functional
when it comes to software design.

This strategy works as follows: We're going to calculate 2 moving averages and when this averages cross
We will sell or buy the stock.

@micheldearaujo
"""

import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf               # Alternative

plt.style.use('dark_background')


# -------------- Defining the parameters -------------------
ma_1 = 7
ma_2 = 15

# Let's define the time frame. How much time we are going to look back into the past
years = 3   # How many years
start = str(dt.datetime.now().date() - dt.timedelta(days=365 * years))  # Starting date
end = str(dt.datetime.now().date()) # Ending date (now)
# Let's get the data through the Pandas DataReader and the Yahoo Finance API.
company = 'TSLA'


class Trader:

    buy_signals = []  # Making a list of the buying signals
    sell_signals = []
    trigger = 0  # This trigger is used to verify the current state of the algorithm

    def __init__(self, company_name):
        self.company_name = company_name

    def get_data(self, company_name, start_date, end_date, ma_1, ma_2):
        # data = web.DataReader(company, 'yahoo', start, end)
        # Getting the data from the yfinance API
        self.data = yf.Ticker(company_name).history(start=start_date, end=end_date)
        print(self.data)

        # Calculate the moving averages
        self.data[f'SMA_{ma_1}'] = self.data['Close'].rolling(window=ma_1).mean()
        self.data[f'SMA_{ma_2}'] = self.data['Close'].rolling(window=ma_2).mean()

        # Filtering the data to start in at the bigger moving average days, because before that there are no values
        self.data = self.data.iloc[ma_2:]
        self.data.to_csv(f'./data/{self.company_name}.csv')
        return self.data

    def get_data_offline(self):
        self.data = pd.read_csv(f'./data/{self.company_name}.csv')
        return self.data

    # Plotting the values
    def plot_initial(self):
        plt.plot(self.data['Close'], label='Share Price', color='lightgray')
        plt.plot(self.data[f'SMA_{ma_1}'], label=f'SMA_{ma_1}', color='orange')
        plt.plot(self.data[f'SMA_{ma_2}'], label=f'SMA_{ma_2}', color='purple')
        plt.title(f'Trading Strategy for {self.company_name} Stocks')
        plt.legend(loc='upper left')
        plt.show()

    # Ok, that the first part: Gathering the data, defining moving averages and making some chats about it.
    # Now we gotta move to the next level: Create a trading strategy to buy and sell at the perfect time.
    # This strategy is based on the crossing of the moving averages. When they cross, we are going to buy or sell

    def execute_trading(self, ma_1, ma_2):

        # Setting the strategy:
        # We will iterate over the dataframe rows and compare the moving averages prices
        for x in range(len(self.data)):

            # If the minor moving average cross up the bigger moving average we will buy the stock
            # Because hypothetically it means that the stock price will increase after that
            if self.data[f'SMA_{ma_1}'].iloc[x] > self.data[f'SMA_{ma_2}'].iloc[x] and self.trigger !=1:
                self.buy_signals.append(data['Close'].iloc[x])
                self.sell_signals.append(float('nan'))
                self.trigger = 1

                # That will happen only if the trigger is not equal to one. Equal to 1 means that the last signal was a 'buy'
                # And we don't want to perform the same action twice.

            # If the smaller moving average crosses down the bigger one, we want to sell the stock
            # because the price will fall after that crossing. And again
            # We are only going to perform this action if the trigger is not equal to -1, the sell signal.
            elif self.data[f'SMA_{ma_1}'].iloc[x] < self.data[f'SMA_{ma_2}'].iloc[x] and self.trigger != -1:
                self.buy_signals.append(float('nan'))
                self.sell_signals.append(data['Close'].iloc[x])
                self.trigger = -1

            # If nothing happens, append a 'nan' to the row.
            else:
                self.buy_signals.append(float('nan'))
                self.sell_signals.append(float('nan'))

        self.data['Buy Signals'] = self.buy_signals
        self.data['Sell Signals'] = self.sell_signals
        
        self.data.index = pd.to_datetime(self.data.Date)
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.plot(data['Close'], label='Share Price', alpha=0.5)
        ax.plot(data[f'SMA_{ma_1}'], label=f'SMA_{ma_1}', color='orange', ls='--')
        ax.plot(data[f'SMA_{ma_2}'], label=f'SMA_{ma_2}', color='purple', ls ='--')
        ax.scatter(data.index, data['Buy Signals'], label='Buy Signals', marker='^', color='#00ff00', lw=3)
        ax.scatter(data.index, data['Sell Signals'], label='Sell Signals', marker='v', color='#ff0000', lw=3)
        ax.set_title(f'Trading Strategy for {company} Stocks')
        ax.legend(loc='upper left')
        plt.grid(alpha=0.2)
        plt.show()

        # The tutorial ends here. Now lets implement some other things to enhance this algorithm and measure how well it is going.

        return self.data

    def evaluate_model(self):
        #  --------- Measuring How well the algorithm is going - Calculating the profits
        # Ok, lets suppose we have 1 Share of the Stock and we are trading it. We need to calculate
        # The profit ratio under the Share initial price.
        # For That we have to subtract the "Sell Signal" column of the "Buy Signal" Column.

        TotalBought = self.data['Buy Signals'].sum()
        TotalSold = self.data['Sell Signals'].sum()
        TotalProfit = TotalSold - TotalBought

        # Well, a negative value. That is because we still have the share and have to sell it to calculate de profit.
        # For now, let's just use the last Close Price of the dataframe as the "actual selling price" to calculate
        # How much profit we would have if we sell that share right now, and the first price of the stocks is the base
        # to calculate de percentage of the profit over the initial value.

        InitialPrice = self.data['Close'].iloc[0]

        # It its necessary to check the trigger. If the last action was a buying action, we need to set the final price
        # as the last price in the data.
        # But if the last action was a selling action, then we do not need to modify the sum.

        if self.trigger == 1:  # Bought
            FinalPrice = self.data['Close'].iloc[len(self.data) -1]
            TotalProfit = round(TotalSold - TotalBought + FinalPrice, 2)
            PercentageProfit = round(TotalProfit * 100, 1)
        else:   # Sold
            TotalProfit = round(TotalSold - TotalBought)
            PercentageProfit = round(TotalProfit / InitialPrice * 100, 1)
        # So:

        print(f'Your total profit was: {TotalProfit} USD\ntogether with the percentege profit: {PercentageProfit}%. \nCongratulations!')

        # Plotting the final result
        self.data.Date = pd.to_datetime(self.data.Date)
        self.data.index = self.data.Date

        fig, ax = plt.subplots(figsize=(12, 8))
        ax.plot(self.data['Close'], label='Share Price', alpha=0.5)
        ax.plot(self.data[f'SMA_{ma_1}'], label=f'SMA_{ma_1}', color='orange', ls='--')
        ax.plot(self.data[f'SMA_{ma_2}'], label=f'SMA_{ma_2}', color='purple', ls ='--')
        ax.scatter(self.data.index, data['Buy Signals'], label='Buy Signals', marker='^', color='#00ff00', lw=3)
        ax.scatter(self.data.index, data['Sell Signals'], label='Sell Signals', marker='v', color='#ff0000', lw=3)
        #plt.text(x=self.data['Date'].mean(),
        #          y=self.data['Close'].max()*.98,
        #          s=f'Total Profit per Share: U${TotalProfit} \nPercentage Profit: {PercentageProfit}%')
        ax.set_title(f'Trading Strategy for {company} Stocks \nTotal Profit per Share: U${TotalProfit} \nPercentage Profit: {PercentageProfit}%', fontsize='18')
        ax.set_xlabel('Date')
        ax.set_ylabel(f'Price (US$)')
        
        plt.legend(loc='upper left')
        plt.grid(alpha=0.2)
        plt.show()
        #image_name = f'{self.company_name}.png'
        #fig.savefig('data/' + image_name)

        return company, TotalProfit, PercentageProfit

trader = Trader(company)
#data = trader.get_data(company, start, end, ma_1, ma_2)
data = trader.get_data_offline()
print("original data", data.info())
new_data = trader.execute_trading(ma_1, ma_2)
print("new data", new_data.info())
results = trader.evaluate_model()


#data = get_data(company, start, end)

## OK, now we now how much profit we got!