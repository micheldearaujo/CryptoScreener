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

    def connect_database(self):
        print("Connecting to the Crypto database")

        self.conn = psycopg2.connect(
                                host="localhost",
                                database="Crypto",
                                user="postgres",
                                password="root"
        )

        self.cur = self.conn.cursor()


    def to_database(self, table_name, date, symbol, name, price, change):
        self.connect_database()

        insert = f"""
                    INSERT INTO {table_name} (date, symbol, name, price, change)
                    values (
                            '{date}',
                            '{symbol}',
                            '{name}',
                           '{price}',
                            '{change}'
                            );
                    """
        
        self.cur.execute(insert)
        self.conn.commit()

        self.cur.close()
        self.conn.close()
    

# Creating a function that gets the cryptocurrencies information with a certain frequency
def get_data(period, symbols, pos):

    db = Database()
    driver = webdriver.Chrome(path)
    driver.get(url)
    sleep(2)

    while True:

        # I have setup this counter variable to select the differents ticker symbols names
        counter = 0
        for j in pos:

            # Getting the elements in the web page
            date = dt.datetime.now()
            symbol = driver.find_element_by_xpath(f'//*[@id="scr-res-table"]/div[1]/table/tbody/tr[{j}]/td[1]/a').text
            name = driver.find_element_by_xpath(f'//*[@id="scr-res-table"]/div[1]/table/tbody/tr[{j}]/td[2]').text
            price = driver.find_element_by_xpath(f'//*[@id="scr-res-table"]/div[1]/table/tbody/tr[{j}]/td[3]/span').text
            price = float(''.join(price.split(','))) # casting it into a number
            change = driver.find_element_by_xpath(f'//*[@id="scr-res-table"]/div[1]/table/tbody/tr[{j}]/td[5]/span').text

            # Saving the information in a CSV file
            f = open(f'./data/{symbols[counter]}.csv', 'a')
            writer = csv.writer(f)
            writer.writerow((date, symbol, name, price, change))
            f.close()

            # Writing down the new information into the database
            print("Writing to DB")
            db.to_database(symbols[counter].lower(), date, symbol, name, price, change)


            # Reading the data from the CSV because it is already organized as a dataframe
            stocks = pd.read_csv(f'./data/{symbols[counter]}.csv')
            print(stocks)


            counter += 1

        sleep(period)





# Creating a new csv
""" for symbol in symbols:
    create_csv(f'./data/{symbol}.csv') """

# Executing the loop
get_data(period, symbols, pos)


