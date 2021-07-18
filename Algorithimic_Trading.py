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
import pandas_datareader as web     # Tradicional, in the tutorial, but not working right now
import yfinance as yf               # Alternative
import smtplib
from base64 import b64encode
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import sys
import os

plt.style.use('dark_background')


# -------------- Defining the parameters -------------------
ma_1 = 30   # 30 Days of Moving Average
ma_2 = 90  # 90 Days of Moving Average

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

    # Creating a email configuration
    @staticmethod
    def config_email(self, text, image_name=None):
        with open(image_name, 'rb') as f:
            img_data = f.read()

        msg = MIMEMultipart()
        keys = open('D:/Projects/emails.txt', 'r').read().splitlines()
        msg['Subject'] = 'Relatório Diário'
        msg['From'] = keys[0]
        msg['To'] = 'Destination email here'

        text = MIMEText(f'{text}')
        msg.attach(text)
        image = MIMEImage(img_data, name=os.path.basename(image_name))
        msg.attach(image)
        return msg

    @staticmethod
    def send_email(self, msg):
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.ehlo()
        s.starttls()
        s.ehlo()

        keys = open('./data/emails.txt', 'r').read().splitlines()
        s.login(keys[0],
                keys[1])

        s.sendmail(msg['From'],
                   msg['To'], msg.as_string())
        s.quit()

    def get_data(self, company_name, start_date, end_date, ma_1, ma_2):
        # data = web.DataReader(company, 'yahoo', start, end)
        self.data = yf.Ticker(company_name).history(start=start_date, end=end_date) # Getting the data from the yfinance API
        print(self.data)

        # Calculate the moving averages
        self.data[f'SMA_{ma_1}'] = self.data['Close'].rolling(window=ma_1).mean()
        self.data[f'SMA_{ma_2}'] = self.data['Close'].rolling(window=ma_2).mean()

        # Filtering the data to start in at the bigger moving average days, because before that there are no values
        self.data = self.data.iloc[ma_2:]
        #self.data.reset_index(inplace=True)
        self.data.to_csv(f'./data/{self.company_name}.csv')
        return self.data

    def get_data_off(self):
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

                # msg = config_email(text=f"Opa meu amigo! Estou aqui olhando as ações da {company} e na data {data.index[x]} você deve"
                #                  f"vender todas as suas ações, cada uma por {data['Close'].iloc[x]}")
                # send_email(msg)

                # That will happen only if the trigger is not equal to one. Equal to 1 means that the last signal was a 'buy'
                # And we don't want to perform the same action twice.

            # If the smaller moving average crosses down the bigger one, we want to sell the stock
            # because the price will fall after that crossing. And again
            # We are only going to perform this action if the trigger is not equal to -1, the sell signal.
            elif self.data[f'SMA_{ma_1}'].iloc[x] < self.data[f'SMA_{ma_2}'].iloc[x] and self.trigger != -1:
                self.buy_signals.append(float('nan'))
                self.sell_signals.append(data['Close'].iloc[x])
                self.trigger = -1

                # msg = config_email(text=f"Opa meu amigo! Estou aqui olhando as ações da {company} e na data {data.index[x]} você deve"
                #                  f"comprar ações, cada uma por {data['Close'].iloc[x]}")
                # send_email(msg)

            # If nothing happens, append a 'nan' to the row.
            else:
                self.buy_signals.append(float('nan'))
                self.sell_signals.append(float('nan'))

        self.data['Buy Signals'] = self.buy_signals
        self.data['Sell Signals'] = self.sell_signals

        print(self.data)

        # plt.plot(data['Close'], label='Share Price', alpha=0.5)
        # plt.plot(data[f'SMA_{ma_1}'], label=f'SMA_{ma_1}', color='orange', ls='--')
        # plt.plot(data[f'SMA_{ma_2}'], label=f'SMA_{ma_2}', color='purple', ls ='--')
        # plt.scatter(data.index, data['Buy Signals'], label='Buy Signals', marker='^', color='#00ff00', lw=3)
        # plt.scatter(data.index, data['Sell Signals'], label='Sell Signals', marker='v', color='#ff0000', lw=3)
        # plt.title(f'Trading Strategy for {company} Stocks')
        # plt.legend(loc='upper left')
        # plt.grid(alpha=0.2)
        # plt.show()

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
        # fig, ax = plt.subplots(figsize=(15, 10))
        # ax.plot(self.data['Close'], label='Share Price', alpha=0.5)
        # ax.plot(self.data[f'SMA_{ma_1}'], label=f'SMA_{ma_1}', color='orange', ls='--')
        # ax.plot(self.data[f'SMA_{ma_2}'], label=f'SMA_{ma_2}', color='purple', ls ='--')
        # ax.scatter(self.data.index, data['Buy Signals'], label='Buy Signals', marker='^', color='#00ff00', lw=3)
        # ax.scatter(self.data.index, data['Sell Signals'], label='Sell Signals', marker='v', color='#ff0000', lw=3)
        # # plt.text(x=self.data['Date'].mean(),
        # #          y=self.data['Close'].max()*.98,
        # #          s=f'Total Profit per Share: U${TotalProfit} \nPercentage Profit: {PercentageProfit}%')
        # ax.set_title(f'Trading Strategy for {company} Stocks \nTotal Profit per Share: U${TotalProfit} \nPercentage Profit: {PercentageProfit}%', fontsize='18')
        # ax.set_xlabel('Date')
        # ax.set_ylabel(f'Price (US$) || MA {ma_1, ma_2}')
        #
        # plt.legend(loc='upper left')
        # plt.grid(alpha=0.2)
        # plt.show()
        # image_name = f'{self.company_name}.png'
        # fig.savefig('data/' + image_name)

        return company, TotalProfit, PercentageProfit

#msg = config_email(image_name=image_name, text=f"Opa meu amigo! Terminamos aqui a análise do período indicado e temos os seguintes resultados.\n"
#                       f"'Total Profit per Share: U${TotalProfit} \n"
#                      f"Percentage Profit: {PercentageProfit}%")
#send_email(msg)


trader = Trader(company)
data = trader.get_data(company, start, end, ma_1, ma_2)
# data = trader.get_data_off()
new_data = trader.execute_trading(ma_1, ma_2)
trader.evaluate_model()


#data = get_data(company, start, end)

## OK, now we now how much profit we got!

# Now it is time to optimize this strategy. What are the "Golden" numbers for the moving averages?
# We gotta test for a bunch of combinations to see what combination performs better.
ma_1 = [7, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180, 195, 210]
ma_2 = [7, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180, 195, 210]
profits = list()
Evaluation = pd.DataFrame()
for j in range(len(ma_1)):
    for k in range(len(ma_2)):
        if ma_1[j] == ma_2[k]:
            pass
        else:
            trader = Trader(company)
            data = trader.get_data(company, start, end, ma_1[j], ma_2[k])
            data = trader.execute_trading(ma_1[j], ma_2[k])
            Company, TotalProfit, PercentageProfit = trader.evaluate_model()
            profits.append(f'{ma_1[j]}, {ma_2[k]}: {TotalProfit}, {PercentageProfit}')

            print(f'{ma_1[j]} and {ma_2[k]}')