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

path = 'C:\Program Files (x86)\chromedriver.exe'
url = 'https://finance.yahoo.com/cryptocurrencies'


period = 3
symbols = ['BTC', 'ETH', 'ADA', 'DOGE', 'LTC']
pos = [1, 2, 5, 9, 13]