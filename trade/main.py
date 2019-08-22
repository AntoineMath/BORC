import sys, os
from time import sleep
import datetime
from binance.client import Client
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
import Data.keys


client = Client(Data.keys.apiKey, Data.keys.secretKey)
print(client)
