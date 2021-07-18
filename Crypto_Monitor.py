"""
In this part of the project I intend to create a script to get streaming data from Yahoo Finance website
And make some decisions about it (Maybe daytrade)

This strategy works as follows: We're going to calculate 2 moving averages and when this averages cross
We will sell or buy the stock.

@micheldearaujo
"""

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import datetime as dt
import csv
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

path = 'C:\Program Files (x86)\chromedriver.exe'
url = 'https://finance.yahoo.com/cryptocurrencies'


def create_csv(file_name):
    f = open(file_name, 'w')
    writer = csv.writer(f)
    writer.writerow(('Date', 'Symbol', 'Name', 'Price', 'Change'))
    f.close()


def get_data(period, symbols, pos):

    driver = webdriver.Chrome(path)
    driver.get(url)
    sleep(4)

    while True:

        counter = 0
        for j in pos:

            date = dt.datetime.now()
            symbol = driver.find_element_by_xpath(f'//*[@id="scr-res-table"]/div[1]/table/tbody/tr[{j}]/td[1]/a').text
            name = driver.find_element_by_xpath(f'//*[@id="scr-res-table"]/div[1]/table/tbody/tr[{j}]/td[2]').text
            price = driver.find_element_by_xpath(f'//*[@id="scr-res-table"]/div[1]/table/tbody/tr[{j}]/td[3]/span').text
            change = driver.find_element_by_xpath(f'//*[@id="scr-res-table"]/div[1]/table/tbody/tr[{j}]/td[5]/span').text

            f = open(f'./data/{symbols[counter]}.csv', 'a')
            writer = csv.writer(f)
            writer.writerow((date, symbol, name, price, change))
            f.close()

            stocks = pd.read_csv(f'./data/{symbols[counter]}.csv')
            print(stocks)

            counter += 1

        plt.plot(stocks['Date'], stocks['Price'])
        plt.title(f"{stocks['Symbol']} price")
        plt.show()
        plt.pause(1)

        sleep(period)


period = 60
symbols = ['BTC', 'ETH', 'ADA', 'DOGE', 'LTC']
pos = [1, 2, 5, 9, 13]
# Creating a new csv
# for symbol in symbols:
#     create_csv(f'./data/{symbol}.csv')

# Executing the loop
get_data(period, symbols, pos)


