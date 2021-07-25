"""
In this part of the project I intend to create a script to get streaming data from Yahoo Finance website
and plot it in real-time with Plotly.
Then I will try to make a dashbord at the end of each day with the most important information about each
crypto currency

@micheldearaujo     created at SUN 2021 July 18 20:30

"""
from config import *



def create_csv(file_name):
    f = open(file_name, 'w')
    writer = csv.writer(f)
    writer.writerow(('Date', 'Symbol', 'Name', 'Price', 'Change'))
    f.close()


class Database():

    def __init__(self):
        pass


    def to_database():
        pass

    
    def update_database():
        pass


    def remove_database():
        pass

# Defining a function to plot the streaming data
""" def plot_data(stocks):
    line.set_xdata(stocks['Date']) # Updating the values without create another canvas
    line.set_ydata(stocks['Price'])
    return line, """


# Creating a function that gets the cryptocurrencies information with a certain frequency
def get_data(period, symbols, pos):

    driver = webdriver.Chrome(path)
    driver.get(url)
    sleep(4)

    while True:

        # I have setup this counter variable to select the differents ticker symbols names
        counter = 0
        for j in pos:

            # Getting the elements in the web page
            date = dt.datetime.now()
            symbol = driver.find_element_by_xpath(f'//*[@id="scr-res-table"]/div[1]/table/tbody/tr[{j}]/td[1]/a').text
            name = driver.find_element_by_xpath(f'//*[@id="scr-res-table"]/div[1]/table/tbody/tr[{j}]/td[2]').text
            price = driver.find_element_by_xpath(f'//*[@id="scr-res-table"]/div[1]/table/tbody/tr[{j}]/td[3]/span').text
            change = driver.find_element_by_xpath(f'//*[@id="scr-res-table"]/div[1]/table/tbody/tr[{j}]/td[5]/span').text

            # Saving the information in a CSV file
            f = open(f'./data/{symbols[counter]}.csv', 'a')
            writer = csv.writer(f)
            writer.writerow((date, symbol, name, price, change))
            f.close()

            # Reading the data from the CSV because it is already organized as a dataframe
            stocks = pd.read_csv(f'./data/{symbols[counter]}.csv')
            print(stocks)


            counter += 1

        sleep(period)


# Creating a function that verifies if the prices follows some conditions
def verify_condition(self):
    pass


# Creating a new csv
for symbol in symbols:
    create_csv(f'./data/{symbol}.csv')

# Executing the loop
get_data(period, symbols, pos)


