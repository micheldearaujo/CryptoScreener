"""
In this part of the project I intend to create a script to get streaming data from Yahoo Finance website
and plot it in real-time with Plotly.
Then I will try to make a dashbord at the end of each day with the most important information about each
crypto currency

@micheldearaujo     created at SUN 2021 July 18 20:30
"""

from config import *
plt.style.use('dark_background')

# Creating a animation function that will plot all the live data

def animate(i):
    j, k = 0, 0
    for l in range(len(symbols)):
        data = pd.read_csv(f'D:\Projects\DataScience\Finance\MonitoringStocks\data\{symbols[l]}.csv')

        # Setting up the variables
        data['Date'] = pd.to_datetime(data['Date'])
        crypto = data['Name'][0].split(' ')[0]

        # Calculating the moving averages
        data[f'SMA_{ma_1}'] = data['Price'].rolling(window=ma_1).mean()
        data[f'SMA_{ma_2}'] = data['Price'].rolling(window=ma_2).mean()


        ax[j,k].cla()
        ax[j,k].plot(data['Date'], data['Price'], label=f'{crypto} Price', color='white')

        # Plotting the moving averages
        ax[j,k].plot(data['Date'], data[f'SMA_{ma_1}'], label=f'SMA_{ma_1}', color= 'orange')
        ax[j,k].plot(data['Date'], data[f'SMA_{ma_2}'], label=f'SMA_{ma_2}', color= 'purple')

        # Calling the trader function
        trigger, bought, sold = verify_condition(data)

        # Evaluatin the model
        totalProfit, percentProfit = evaluate_model(data, trigger)

        # Now scatter the trading signals into the figure
        ax[j,k].scatter(data['Date'], data['Buy_Signals'], label="Buy Signal", marker='^', color='#00ff00', lw=3)
        ax[j,k].scatter(data['Date'], data['Sell_Signals'], label="Sell Signal", marker='v', color='#ff0000', lw=3)

        # Writing the profit text in the chart
        ax[j,k].text(x=data['Date'].mean(),
                    y= data['Price'].max()*0.993,
                    s=f'Total profit per share: U$ {totalProfit} \nPercent profit: {percentProfit}% \nBought: {bought} \nSould: {sold}')

        # Configs
        ax[j,k].set_xlabel('Time')
        ax[j,k].set_ylabel('Price (USD)')
        ax[j,k].set_title(f'{crypto} Price today {str(dt.datetime.now().date())}')
        ax[j,k].legend(loc='lower left')
        plt.tight_layout()
        ax[j,k].grid(alpha=0.2)

        # This set of ifs is itereate over the 2-dimensional axis of the subplot figure.
        # I have not found a better way to do it, but it is working.
        if (j == 0 and k == 0):
            j, k = 0, 1

        elif (j ==0 and k == 1):
            j, k = 1, 0

        elif (j == 1 and k == 0):
            j, k = 1, 1

        else:
            j, k = 0, 0


# Creating a function that verifies if the prices follows some conditions
def verify_condition(data):
    trigger = 0
    buy_signals = []
    sell_signals = []
    bought = 0
    sold = 0
    # Setting up the strategy:
    # I will iterate over the dataframe rows and compare the moving averages prices

    for x in range(len(data)):
        # TODO: The way this function is writen it will verify all the dataframe multiple times.
        # TODO: The best way to go through this is to check only the last line...

        # If the shorter moving average crosses up the longer moving average it will emit a signal to buy the share
        # Because hypothetically it means that the cryptocurrency (or stock) will increase after that.
        # And it is necessary to set up a variable that identifies if a action (buy or sell) has already being made.
        # I do not want that the same action is taken in sequency.
        if data[f'SMA_{ma_1}'].iloc[x] > data[f'SMA_{ma_2}'].iloc[x] and trigger !=1:
            buy_signals.append(data['Price'].iloc[x])
            sell_signals.append(float('nan'))

            # After the action has being taken, I settup the trigger to 1
            # To mark that a buy action took place
            trigger = 1
            bought += 1
        

        # If the shorter moving average crosses down the bigger one it will emit a signal to sell the share
        # Because the share price will fall after that.
        elif data[f'SMA_{ma_1}'].iloc[x] < data[f'SMA_{ma_2}'].iloc[x] and trigger !=-1:
            buy_signals.append(float('nan'))
            sell_signals.append(data['Price'].iloc[x])
            trigger = -1
            sold += 1

        else: 
            buy_signals.append(float('nan'))
            sell_signals.append(float('nan'))

    # After that we add the new points to the dataframe.
    data['Buy_Signals'] = buy_signals
    data['Sell_Signals'] = sell_signals

    return trigger, bought, sold


def evaluate_model(data, trigger):
    
    # ----- Measuring how well the algorithm is going - calculating the profits
    # Ok, lets suppose that we have 1 share of each scryptocurrency and we trading it (buying one or selling one). We need
    # to calculate the profit ratio under the share initial price.
    # For that we have to subtract the "Buy signal" column from the "Sell signal" column.

    totalBought = data['Buy_Signals'].sum()
    totalSold = data['Sell_Signals'].sum()
    totalProfit = totalSold - totalBought

    # If I define those variables like that one thing that can happen is a negative profit because I still have the share and the algorithm does not
    # took into account its actual value. To correct that I will use the last price of the dataframe as the "actual selling price" to calculate
    # how much profit I would have if I sell the share right now. The first price of the stock is the base to calculate the percentage
    # of the profit over the initial price.

    initialPrice = data['Price'].iloc[0]

    # It is necessary to check the trigger value. If the last action was a buying action then I need to set the final price as the last price
    # in the dataset. Otherwise, I do not need to modify it.

    if trigger == 1: # if the last action was a buying
        finalPrice = data['Price'].iloc[len(data)-1]
        totalProfit = round(totalSold - totalBought + finalPrice, 3)
        percentProfit = round(totalProfit/initialPrice * 100, 2)
    
    else:   # Sold
        totalProfit = round(totalSold - totalBought)
        percentProfit = round(totalProfit/initialPrice * 100, 2)


    # And returns the values to show in the charts
    return totalProfit, percentProfit




# Creating a figure
fig, ax = plt.subplots(2, 2, clear=True)

# Starting the animation
animation = FuncAnimation(fig, animate, interval=period*1000)

plt.show()