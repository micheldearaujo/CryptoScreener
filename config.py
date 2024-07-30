#  This file contains all the parameters used
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import datetime as dt
import csv
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
# import psycopg2

path = 'C:\Program Files (x86)\chromedriver.exe'
url = 'https://finance.yahoo.com/cryptocurrencies'

# Frequency of reading
period = 3

# Some Cryptocurrencies to watch
symbols = ['BTC', 'ADA', 'DOGE', 'LTC']
names = ['Bitcoin', 'Cardano', 'Dogecoin', 'Litecoin']
pos = [1, 5, 7, 13]

# Moving averages in seconds
ma_1 = 90
ma_2 = 150

