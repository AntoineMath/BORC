import data.keys
import sys
import os
from time import sleep
import datetime
from binance.client import Client
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

CLIENT = Client(data.keys.apiKey, data.keys.secretKey)
TIME_START = datetime.datetime.now()
print(CLIENT)
