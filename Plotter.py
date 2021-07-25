from config import *

# Creating a animation function that will plot all the live data
def animate(i):
    data = pd.read_csv('D:\Projects\DataScience\Finance\MonitoringStocks\data\LTC.csv')
    data['Date'] = pd.to_datetime(data['Date'])
    x = data['Date']
    y = data['Price']

    plt.cla()
    plt.plot(x, y, label='Litecoin Price today')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.title('Litecoin Price')

    plt.legend(loc='upper left')
    plt.tight_layout()
    plt.grid()

#fig, ax = plt.subplots(3, 2)


animation = FuncAnimation(plt.gcf(), animate, interval=period*1000)


plt.show()