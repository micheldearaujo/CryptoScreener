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
        x = data['Date']
        y = data['Price']

        # Calculating the moving averages
        data[f'SMA_{ma_1}'] = data['Price'].rolling(window=ma_1).mean()
        data[f'SMA_{ma_2}'] = data['Price'].rolling(window=ma_2).mean()


        ax[j,k].cla()
        ax[j,k].plot(x, y, label=f'{crypto} Price', color='white')

        # Plotting the moving averages
        ax[j,k].plot(x, data[f'SMA_{ma_1}'], label=f'SMA_{ma_1}', color= 'orange')
        ax[j,k].plot(x, data[f'SMA_{ma_2}'], label=f'SMA_{ma_2}', color= 'purple')

        ax[j,k].set_xlabel('Time')
        ax[j,k].set_ylabel('Price (USD)')
        ax[j,k].set_title(f'{crypto} Price today {str(dt.datetime.now().date())}')

        ax[j,k].legend(loc='upper left')
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



# Creating a figure
fig, ax = plt.subplots(2, 2, clear=True)

# Starting the animation
animation = FuncAnimation(fig, animate, interval=period*1000)

plt.show()