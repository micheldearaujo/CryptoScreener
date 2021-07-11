"""
In this Project i will follow NeuralNine tutorial on Algorithmic Trading Strategy
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
import matplotlib.pyplot as plt
import pandas_datareader as web     # Tradicional, in the tutorial, but not working right now
import yfinance as yf               # Alternative
import smtplib
from base64 import b64encode
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import sys, os

plt.style.use('dark_background')


# -------------- Defining the parameters -------------------
ma_1 = 30   # 30 Days of Moving Average
ma_2 = 90  # 100 Days of Moving Average

# Let's define the time frame. That how much time we are going to look back into the past
years = 3   # How many years
start = str(dt.datetime.now().date() - dt.timedelta(days=365 * years))  # Starting date
end = str(dt.datetime.now().date()) #    Ending date (now)
# Let's get the data through the Pandas DataReader and the Yahoo Finance API.
company = 'TSLA'

def config_email(text,image_name=None):
    with open(image_name, 'rb') as f:
        img_data = f.read()

    msg = MIMEMultipart()
    msg['Subject'] = 'Relatório Diário'
    msg['From'] = 'michelarrudala@gmail.com'
    msg['To'] = 'viniciusfarah42@gmail.com'

    text = MIMEText(f'{text}')
    msg.attach(text)
    image = MIMEImage(img_data, name=os.path.basename(image_name))
    msg.attach(image)
    return msg

def send_email(msg):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.ehlo()

    s.login('michelarrudala@gmail.com',
            '86558179')

    s.sendmail(msg['From'],
               msg['To'], msg.as_string())
    s.quit()

def get_data(company_name, start_date, end_date):
    #data = web.DataReader(company, 'yahoo', start, end)
    data = yf.Ticker(company_name).history(start=start_date, end=end_date) # Getting the data from the yfinance API
    print(data)

    # Calculate the moving averages
    data[f'SMA_{ma_1}'] = data['Close'].rolling(window=ma_1).mean()
    data[f'SMA_{ma_2}'] = data['Close'].rolling(window=ma_2).mean()

    # Filtering the data to start in at the bigger moving average days, because before that there are no values
    data = data.iloc[ma_2:]

    return(data)

data = get_data(company, start, end)

# Plotting the values
def plot_initial(data):
    plt.plot(data['Close'], label='Share Price', color='lightgray')
    plt.plot(data[f'SMA_{ma_1}'], label=f'SMA_{ma_1}', color='orange')
    plt.plot(data[f'SMA_{ma_2}'], label=f'SMA_{ma_2}', color='purple')
    plt.title(f'Trading Strategy for {company} Stocks')
    plt.legend(loc='upper left')
    plt.show()

# Ok, that the first part: Gathering the data, defining moving averages and making some chats about it.
# Now we gotta move to the next level: Create a trading strategy to buy and sell at the perfect time.
# This strategy is based on the crossing of the moving averages. When they cross, we are going to buy or sell

#def execute_trading(data):
buy_signals = []        # Making a list of the buying signals
sell_signals = []
trigger = 0             # This trigger is used to verify the current state of the algorithm

# Setting the strategy:
# We will iterate over the dataframe rows and compare the moving averages prices
for x in range(len(data)):
    # If the minor moving average cross up the bigger moving average we will buy the stock
    # Because hypothetically it means that the stock price will increase after that
    if data[f'SMA_{ma_1}'].iloc[x] > data[f'SMA_{ma_2}'].iloc[x] and trigger !=1:
        buy_signals.append(data['Close'].iloc[x])
        sell_signals.append(float('nan'))
        trigger = 1

        msg = config_email(text=f"Opa meu amigo! Estou aqui olhando as ações da {company} e na data {data.index[x]} você deve"
                           f"vender todas as suas ações, cada uma por {data['Close'].iloc[x]}")
        send_email(msg)

        # That will happen only if the trigger is not equal to one. Equal to 1 means that the last signal was a 'buy'
        # And we don't want to perform the same action twice.

    # If the smaller moving average crosses down the bigger one, we want to sell the stock
    # because the price will fall after that crossing. And again
    # We are only going to perform this action if the trigger is not equal to -1, the sell signal.
    elif data[f'SMA_{ma_1}'].iloc[x] < data[f'SMA_{ma_2}'].iloc[x] and trigger !=-1:
        buy_signals.append(float('nan'))
        sell_signals.append(data['Close'].iloc[x])
        trigger = -1

        msg = config_email(text=f"Opa meu amigo! Estou aqui olhando as ações da {company} e na data {data.index[x]} você deve"
                           f"comprar ações, cada uma por {data['Close'].iloc[x]}")
        send_email(msg)

    # If nothing happens, append a 'nan' to the row.
    else:
        buy_signals.append(float('nan'))
        sell_signals.append(float('nan'))

data['Buy Signals'] = buy_signals
data['Sell Signals'] = sell_signals
#return data
#data = execute_trading(data)

print(data)

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


# Measuring How well the algorithm is going - Calculating the profits
# Ok, lets suppose we have 1 Share of the Stock and we are trading it. We need to calculate
# The profit ratio under the Share initial price.
# For That we have to subtract the "Sell Signal" column of the "Buy Signal" Column.

TotalBought = data['Buy Signals'].sum()
TotalSold = data['Sell Signals'].sum()
TotalProfit = TotalSold - TotalBought
print(TotalProfit)

# Well, a negative value. That is because we still have the share and have to sell it to calculate de profit.
# For now, let's just use the last Close Price of the dataframe as the "actual selling price" to calculate
# How much profit we would have if we sell that share right now, and the first price of the stocks is the base
# to calculate de percentage of the profit over the initial value.

InitialPrice = data['Close'].iloc[0]

# It its necessary to check the trigger. If the last action was a buying action, we need to set the final price
# as the last price in the data.
# But if the last action was a selling action, then we do not need to modify the sum.
if trigger==1: # Bought
    FinalPrice = data['Close'].iloc[len(data) -1]
    TotalProfit = round(TotalSold - TotalBought + FinalPrice, 2)
    PercentageProfit = round(TotalProfit / InitialPrice * 100, 1)
else:   # Sold
    TotalProfit = round(TotalSold - TotalBought)
    PercentageProfit = round(TotalProfit / InitialPrice * 100, 1)
# So:


# Plotting the final result
fig, ax = plt.subplots(figsize=(15,10))

ax.plot(data['Close'], label='Share Price', alpha=0.5)
ax.plot(data[f'SMA_{ma_1}'], label=f'SMA_{ma_1}', color='orange', ls='--')
ax.plot(data[f'SMA_{ma_2}'], label=f'SMA_{ma_2}', color='purple', ls ='--')
ax.scatter(data.index, data['Buy Signals'], label='Buy Signals', marker='^', color='#00ff00', lw=3)
ax.scatter(data.index, data['Sell Signals'], label='Sell Signals', marker='v', color='#ff0000', lw=3)
plt.text(x=data.index.mean(),
         y=data['Close'].max()*.98,
         s=f'Total Profit per Share: U${TotalProfit} \nPercentage Profit: {PercentageProfit}%')
ax.set_title(f'Trading Strategy for {company} Stocks', fontsize='18')
ax.set_xlabel('Date')
ax.set_ylabel('Price (US$')

plt.legend(loc='upper left')
plt.grid(alpha=0.2)
plt.show()
image_name = 'stocks.png'
fig.savefig(image_name)

msg = config_email(image_name=image_name, text=f"Opa meu amigo! Terminamos aqui a análise do período indicado e temos os seguintes resultados.\n"
                        f"'Total Profit per Share: U${TotalProfit} \n"
                        f"Percentage Profit: {PercentageProfit}%")
send_email(msg)



## OK, now we now how much profit we got!

# Now it is time to optimize this strategy. What are the "Golden" numbers for the moving averages?
# We gotta test for a bunch of combinations to see what combination performs better.
ma_1 = [7, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180, 195, 210]
ma_2 = [7, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180, 195, 210]